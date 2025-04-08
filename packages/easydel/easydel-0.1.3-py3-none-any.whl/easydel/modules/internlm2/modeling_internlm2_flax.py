# Copyright 2023 The EASYDEL Author @erfanzar (Erfan Zare Chavoshi).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import functools
import typing as tp

import chex
import jax
import jax.numpy as jnp
from einops import rearrange
from flax import nnx as nn

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import (
	BaseModelOutput,
	CausalLMOutput,
	SequenceClassifierOutput,
)
from easydel.infra.utils import (
	ACT2FN,
	auto_remat,
	block_wise_ffn,
	control_mlp_sharding,
	get_dot_general_by_bits,
)
from easydel.layers.attention import AttentionModule, FlexibleAttentionModule
from easydel.layers.caching import (
	PagedAttentionCache,
	PagedAttentionCacheView,
	PagedAttentionMetadata,
	TransformerCache,
	TransformerCacheView,
	TransformerMetadata,
)
from easydel.layers.linear import ParallelLinear
from easydel.layers.norms import RMSNorm

from .internlm2_configuration import InternLM2Config


class InternLM2Attention(AttentionModule):
	"""InternLM2 Attention module.

	Attributes:
	    config (InternLM2Config): Configuration object for the model.
	    dtype (jnp.dtype): Data type for computation. Default is jnp.float32.
	    param_dtype (jnp.dtype): Data type for parameters. Default is jnp.float32.
	    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Default is None.
	    rngs (nn.Rngs): Random number generators.
	    hidden_size (int): Dimensionality of the hidden states.
	    num_heads (int): Number of attention heads.
	    head_dim (int): Dimensionality of each attention head.
	    num_key_value_heads (int): Number of key/value heads (for GQA).
	    num_key_value_groups (int): Number of query head groups for each key/value head.
	    max_position_embeddings (int): Maximum sequence length supported.
	    wqkv (ParallelLinear): Linear layer for query, key, and value projections.
	    wo (ParallelLinear): Linear layer for the output projection.
	    attention_performer (FlexibleAttentionModule): Module to perform the core attention computation.
	    rotary (RoPE): Rotary position embedding module.
	"""

	def __init__(
		self,
		config: InternLM2Config,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		"""Initializes the InternLM2Attention module.

		Args:
		    config (InternLM2Config): The configuration object for the InternLM2 model.
		    dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
		    param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
		    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
		    rngs (nn.Rngs): Random number generators.
		"""
		super().__init__(config=config)
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		self.rngs = rngs
		self.hidden_size = config.hidden_size
		self.num_heads = config.num_attention_heads
		self.head_dim = self.hidden_size // self.num_heads
		self.num_key_value_heads = config.num_key_value_heads
		self.num_key_value_groups = self.num_heads // self.num_key_value_heads
		self.max_position_embeddings = config.max_position_embeddings
		if (self.head_dim * self.num_heads) != self.hidden_size:
			raise ValueError(
				f"hidden_size must be divisible by num_heads (got `hidden_size`: {self.hidden_size}"
				f" and `num_heads`: {self.num_heads})."
			)
		self.wqkv = ParallelLinear(
			config.hidden_size,
			(self.num_heads + 2 * self.num_key_value_heads) * self.head_dim,
			dtype=dtype,
			param_dtype=param_dtype,
			use_bias=config.bias,
			rngs=rngs,
			kernel_init=jax.nn.initializers.normal(config.initializer_range),
			precision=precision,
			**get_dot_general_by_bits(config.bits, config.easy_method),
		)
		self.wo = ParallelLinear(
			self.num_heads * self.head_dim,
			config.hidden_size,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
			use_bias=config.bias,
			kernel_init=jax.nn.initializers.normal(config.initializer_range),
			precision=precision,
			**get_dot_general_by_bits(config.bits, config.easy_method),
		)

		self.attention_performer = FlexibleAttentionModule(
			base_config=config,
			softmax_scale=self.head_dim**-0.5,
			dropout_prob=0.0,
		)

		self.rotary = self.config.get_basic_rope(
			dtype=self.dtype,
			head_size=self.head_dim,
			rotary_dim=self.head_dim,
			base=config.rope_theta,
		)

	def __call__(
		self,
		hidden_states: chex.Array,
		attention_mask: chex.Array,
		position_ids: chex.Array,
		causal_mask: tp.Optional[chex.Array | bool],
		cache_view: tp.Optional[TransformerCacheView | PagedAttentionCacheView] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: bool = False,
		fcm_mask: tp.Optional[chex.Array] = None,
		frequencies: tp.Optional[chex.Array] = None,
	):
		"""
		Forward pass of the attention module.

		Args:
		    hidden_states (chex.Array): Input hidden states.
		    attention_mask (chex.Array): Mask to apply on the attention scores.
		    position_ids (chex.Array): Position indices for the tokens.
		    causal_mask (chex.Array): Causal mask for ensuring autoregressive behavior.
		    segment_ids (tp.Optional[chex.Array]): Segment IDs for segment-based attention (optional).
		    deterministic (bool): If True, disables dropout for deterministic behavior.
		    init_cache (bool): If True, initializes cache for caching keys and values.
		    output_attentions (bool): If True, outputs attention weights alongside the hidden states.
		    fcm_mask (tp.Optional[chex.Array]): fcm mask to be combined with attn mask and causal mask.
		Returns:
		    tp.Tuple[chex.Array, chex.Array]: A tuple containing the attention output and the attention weights.
		"""
		qkv_states = rearrange(
			self.wqkv(hidden_states),
			"b q (h gs d) -> b q h gs d",
			gs=2 + self.num_key_value_groups,
			d=self.head_dim,
		)

		query_states = qkv_states[..., : self.num_key_value_groups, :]
		query_states = rearrange(query_states, "b q h gs d -> b q (h gs) d")
		key_states = qkv_states[..., -2, :]
		value_states = qkv_states[..., -1, :]
		query_states, key_states = self.rotary(
			query=query_states,
			key=key_states,
			positions=position_ids,
			frequencies=frequencies,
		)

		(
			key_states,
			value_states,
			attention_mask,
			init_attention_bias,
		) = self.concatenate(
			query=query_states,
			key=key_states,
			cache_view=cache_view,
			value=value_states,
			attention_mask=attention_mask,
			causal_mask=causal_mask,
			fcm_mask=fcm_mask,
		)

		attentions = self.attention_performer.forward(
			query_states=query_states,
			key_states=key_states,
			value_states=value_states,
			bias=None,
			cache_metadata=cache_metadata,
			cache_view=cache_view,
			init_bias=init_attention_bias,
			attention_mask=attention_mask,
			segment_ids=segment_ids,
			causal=True,
			dropout_rng=self.rngs.params(),
		)

		attn_output = self.wo(
			self.shard_attention_prod(self._merge_heads(attentions.attention_outputs))
		)

		outputs = (
			(attn_output, attentions.attention_weights)
			if output_attentions
			else (attn_output,)
		)
		return outputs


class InternLM2MLP(nn.Module):
	"""InternLM2 MLP module.

	Attributes:
	    config (InternLM2Config): Configuration object for the model.
	    dtype (jnp.dtype): Data type for computation. Default is jnp.float32.
	    param_dtype (jnp.dtype): Data type for parameters. Default is jnp.float32.
	    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Default is None.
	    w1 (ParallelLinear): First linear transformation (gate projection).
	    w3 (ParallelLinear): Second linear transformation (up projection).
	    w2 (ParallelLinear): Third linear transformation (down projection).
	    act_fn (callable): Activation function (e.g., SiLU).
	"""

	def __init__(
		self,
		config: InternLM2Config,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		"""Initializes the InternLM2MLP module.

		Args:
		    config (InternLM2Config): The configuration object for the InternLM2 model.
		    dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
		    param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
		    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
		    rngs (nn.Rngs): Random number generators.
		"""
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		linear = functools.partial(
			ParallelLinear,
			dtype=dtype,
			param_dtype=param_dtype,
			use_bias=False,
			kernel_init=jax.nn.initializers.normal(config.initializer_range),
			precision=self.precision,
			**get_dot_general_by_bits(config.bits, config.easy_method),
		)
		self.w1 = linear(config.hidden_size, config.intermediate_size, rngs=rngs)
		self.w3 = linear(config.hidden_size, config.intermediate_size, rngs=rngs)
		self.w2 = linear(config.intermediate_size, config.hidden_size, rngs=rngs)
		self.act_fn = ACT2FN[config.hidden_act]

	def __call__(self, hidden_states: jnp.ndarray) -> jnp.ndarray:
		"""Forward pass of the MLP module.

		Args:
		    hidden_states (jnp.ndarray): Input hidden states.

		Returns:
		    jnp.ndarray: Output hidden states after MLP transformation.
		"""
		hidden_states = control_mlp_sharding(hidden_states, self.config.partition_axis)
		return self.w2(self.act_fn(self.w1(hidden_states)) * self.w3(hidden_states))


class InternLM2Block(nn.Module):
	"""InternLM2 Transformer Block.

	This module combines the self-attention layer and the MLP layer with residual connections
	and layer normalization.

	Attributes:
	    config (InternLM2Config): Configuration object for the model.
	    dtype (jnp.dtype): Data type for computation. Default is jnp.float32.
	    param_dtype (jnp.dtype): Data type for parameters. Default is jnp.float32.
	    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Default is None.
	    attention (InternLM2Attention): The self-attention module.
	    feed_forward (InternLM2MLP): The feed-forward (MLP) module.
	    attention_norm (RMSNorm): Layer normalization before the attention layer.
	    ffn_norm (RMSNorm): Layer normalization before the MLP layer.
	"""

	def __init__(
		self,
		config: InternLM2Config,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		"""Initializes the InternLM2Block module.

		Args:
		    config (InternLM2Config): The configuration object for the InternLM2 model.
		    dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
		    param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
		    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
		    rngs (nn.Rngs): Random number generators.
		"""
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		attn_block = InternLM2Attention
		mlp_block = InternLM2MLP
		attn_block, mlp_block = auto_remat(
			attn_block,
			mlp_block,
			policy=config.gradient_checkpointing,
		)

		self.attention = attn_block(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

		self.feed_forward = mlp_block(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.attention_norm = RMSNorm(
			dim=config.hidden_size,
			eps=config.rms_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		self.ffn_norm = RMSNorm(
			dim=config.hidden_size,
			eps=config.rms_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)

	def __call__(
		self,
		hidden_states: chex.Array,
		attention_mask: chex.Array,
		position_ids: chex.Array,
		causal_mask: tp.Optional[chex.Array | bool],
		cache_view: tp.Optional[TransformerCacheView | PagedAttentionCacheView] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: bool = False,
		fcm_mask: tp.Optional[chex.Array] = None,
		frequencies: tp.Optional[chex.Array] = None,
	):
		"""Forward pass of the InternLM2Block.

		Applies self-attention, followed by a residual connection and layer normalization,
		and then applies the MLP layer, followed by another residual connection and layer normalization.

		Args:
		    hidden_states (chex.Array): Input hidden states.
		    attention_mask (chex.Array): Mask to apply on the attention scores.
		    position_ids (chex.Array): Position indices for the tokens.
		    causal_mask (tp.Optional[chex.Array | bool]): Causal mask for autoregressive behavior.
		    cache_view (tp.Optional[TransformerCacheView | PagedAttentionCacheView]): Cache view for attention KVs.
		    cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
		    segment_ids (tp.Optional[chex.Array]): Segment IDs (unused in standard InternLM2).
		    output_attentions (bool): Whether to return attention weights. Default is False.
		    fcm_mask (tp.Optional[chex.Array]): Flash Chunking Mask (FCM) for attention.
		    frequencies (tp.Optional[chex.Array]): Precomputed rotary frequency embeddings.

		Returns:
		    tp.Union[tp.Tuple[chex.Array, chex.Array], tp.Tuple[chex.Array]]:
		        A tuple containing the output hidden states. If `output_attentions` is True,
		        it also includes the attention weights.
		"""
		attn_outputs = self.attention(
			self.attention_norm(hidden_states),
			attention_mask,
			position_ids,
			causal_mask,
			cache_view,
			cache_metadata,
			segment_ids,
			output_attentions,
			fcm_mask,
			frequencies,
		)
		attn_output = attn_outputs[0]
		hidden_states = hidden_states + attn_output

		feed_forward_input = self.ffn_norm(hidden_states)

		if self.config.use_scan_mlp:
			feed_forward_hidden_states = block_wise_ffn(
				self.feed_forward, feed_forward_input, self.config.scan_mlp_chunk_size
			)
		else:
			feed_forward_hidden_states = self.feed_forward(feed_forward_input)

		hidden_states = hidden_states + feed_forward_hidden_states

		return (hidden_states,) + attn_outputs[1:]


@register_module(
	TaskType.BASE_MODULE,
	config=InternLM2Config,
	model_type="internlm2",
)
class InternLM2Model(EasyDeLBaseModule):
	"""The base InternLM2 model transformer.

	This class represents the core transformer architecture of the InternLM2 model,
	consisting of embedding layers, multiple transformer blocks, and a final
	layer normalization.

	Attributes:
	    config (InternLM2Config): Configuration object for the model.
	    dtype (jnp.dtype): Data type for computation. Default is jnp.float32.
	    param_dtype (jnp.dtype): Data type for parameters. Default is jnp.float32.
	    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Default is None.
	    embed_tokens (nn.Embed): Embedding layer for input tokens.
	    layers (tp.Sequence[InternLM2Block]): Sequence of transformer blocks.
	    norm (RMSNorm): Final layer normalization.
	    gradient_checkpointing (EasyDeLGradientCheckPointers): Gradient checkpointing configuration.
	    scan_layers (bool): Whether to use JAX scan for layer processing.
	    blocks_class (InternLM2Block): The class used for the transformer blocks.
	"""

	def __init__(
		self,
		config: InternLM2Config,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		"""Initializes the InternLM2Model.

		Args:
		    config (InternLM2Config): The configuration object for the InternLM2 model.
		    dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
		    param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
		    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
		    rngs (nn.Rngs): Random number generators.
		"""
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

		self.tok_embeddings = nn.Embed(
			config.vocab_size,
			config.hidden_size,
			embedding_init=jax.nn.initializers.normal(stddev=config.initializer_range),
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		self.layers = [
			InternLM2Block(
				config=config,
				rngs=rngs,
				dtype=dtype,
				param_dtype=param_dtype,
				precision=precision,
			)
			for i in range(config.num_hidden_layers)
		]
		self.norm = RMSNorm(
			dim=config.hidden_size,
			eps=config.rms_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)

	def __call__(
		self,
		input_ids: tp.Optional[chex.Array] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: tp.Optional[bool] = None,
		output_hidden_states: tp.Optional[bool] = None,
		past_key_values: tp.Optional[TransformerCache | PagedAttentionCache] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		return_dict: bool = True,
	) -> tp.Union[BaseModelOutput, tp.Tuple]:
		"""Forward pass of the InternLM2Model.

		Args:
		    input_ids (tp.Optional[chex.Array]): Input token IDs. Shape: (batch_size, sequence_length).
		    inputs_embeds (tp.Optional[chex.Array]): Input embeddings. Shape: (batch_size, sequence_length, hidden_size).
		        Either `input_ids` or `inputs_embeds` must be provided.
		    attention_mask (tp.Optional[chex.Array]): Mask to avoid performing attention on padding token indices.
		        Shape: (batch_size, sequence_length).
		    position_ids (tp.Optional[chex.Array]): Position indices for the tokens.
		        Shape: (batch_size, sequence_length).
		    segment_ids (tp.Optional[chex.Array]): Segment IDs (unused).
		    output_attentions (tp.Optional[bool]): Whether to return attention weights. Defaults to `config.output_attentions`.
		    output_hidden_states (tp.Optional[bool]): Whether to return hidden states for all layers.
		        Defaults to `config.output_hidden_states`.
		    past_key_values (tp.Optional[TransformerCache | PagedAttentionCache]): Precomputed key/value states for attention.
		    cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
		    return_dict (bool): Whether to return a `BaseModelOutput` object or a tuple.

		Returns:
		    tp.Union[BaseModelOutput, tp.Tuple]: The model's output. If `return_dict` is True,
		        returns a `BaseModelOutput` object containing `last_hidden_state`, `hidden_states` (optional),
		        and `attentions` (optional). Otherwise, returns a tuple with these elements.

		Raises:
		    ValueError: If neither `input_ids` nor `inputs_embeds` is provided.
		"""
		if inputs_embeds is None and input_ids is not None:
			inputs_embeds = self.tok_embeddings(input_ids.astype("i4"))
		else:
			raise ValueError("you should specify inputs_embeds or input_ids one of them")
		batch_size, sequence_length = inputs_embeds.shape[:2]

		if attention_mask is None:
			attention_mask = jnp.ones((batch_size, sequence_length), "b1")
		else:
			if attention_mask.dtype != jnp.bool:
				attention_mask = jnp.astype(attention_mask == 1, "b1")
		if position_ids is None:
			position_ids = jnp.broadcast_to(
				jnp.clip(jnp.cumsum(attention_mask, axis=-1) - 1, a_min=0),
				(batch_size, sequence_length),
			)

		assert sequence_length <= self.config.max_position_embeddings, (
			f"Maximum Position Embedding Reached ! (Excepted <= {self.config.max_position_embeddings} got {sequence_length})"
		)
		if attention_mask.ndim == 2:
			attention_mask = jnp.expand_dims(attention_mask, (1, 2))

		hidden_states = inputs_embeds

		if past_key_values is None:
			past_key_values = TransformerCache.init_empty(len(self.layers))
		all_attentions = () if output_attentions else None
		all_hidden_states = () if output_hidden_states else None

		for idx, block in enumerate(self.layers):
			if output_hidden_states:
				all_hidden_states += (hidden_states,)

			layer_outputs = block(
				hidden_states=hidden_states,
				attention_mask=attention_mask,
				position_ids=position_ids,
				causal_mask=self.causal_mask,
				cache_view=past_key_values.views[idx],
				cache_metadata=cache_metadata,
				output_attentions=output_attentions,
				segment_ids=segment_ids,
				frequencies=self.frequencies,
			)
			hidden_states = layer_outputs[0]

			if output_attentions:
				all_attentions += (layer_outputs[1],)

		hidden_states = self.norm(hidden_states)

		if output_hidden_states:
			all_hidden_states += (hidden_states,)
		outputs = (hidden_states, all_hidden_states, all_attentions, past_key_values)

		if not return_dict:
			return tuple(v for v in outputs if v is not None)

		return BaseModelOutput(
			last_hidden_state=hidden_states,
			hidden_states=all_hidden_states,
			attentions=all_attentions,
			past_key_values=past_key_values,
		)


@register_module(
	TaskType.CAUSAL_LM,
	config=InternLM2Config,
	model_type="internlm2",
)
class InternLM2ForCausalLM(EasyDeLBaseModule):
	"""InternLM2 model with a Causal Language Modeling head.

	This model consists of the base InternLM2 transformer (`InternLM2Model`) followed by a
	linear layer (`lm_head`) that projects the transformer's output hidden states
	to the vocabulary size, producing logits for next token prediction.

	Attributes:
	    config (InternLM2Config): Configuration object for the model.
	    dtype (jnp.dtype): Data type for computation. Default is jnp.float32.
	    param_dtype (jnp.dtype): Data type for parameters. Default is jnp.float32.
	    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Default is None.
	    rngs (nn.Rngs): Random number generators.
	    module (InternLM2Model): The core InternLM2 transformer model.
	    lm_head (ParallelLinear): The linear layer for projecting hidden states to vocabulary logits.
	"""

	def __init__(
		self,
		config: InternLM2Config,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		"""Initializes the InternLM2ForCausalLM model.

		Args:
		    config (InternLM2Config): The configuration object for the InternLM2 model.
		    dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
		    param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
		    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
		    rngs (nn.Rngs): Random number generators.
		"""
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

		self.model = InternLM2Model(
			config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

		self.output = ParallelLinear(
			config.hidden_size,
			config.vocab_size,
			dtype=dtype,
			param_dtype=param_dtype,
			use_bias=False,
			rngs=rngs,
			kernel_init=jax.nn.initializers.normal(stddev=config.initializer_range),
			precision=precision,
			**get_dot_general_by_bits(config.bits, config.easy_method),
		)

	def __call__(
		self,
		input_ids: tp.Optional[chex.Array] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		output_attentions: tp.Optional[bool] = None,
		output_hidden_states: tp.Optional[bool] = None,
		past_key_values: tp.Optional[TransformerCache | PagedAttentionCache] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		return_dict: bool = True,
	) -> tp.Union[CausalLMOutput, tp.Tuple]:
		"""Forward pass of the InternLM2ForCausalLM model.

		Args:
		    input_ids (tp.Optional[chex.Array]): Input token IDs. Shape: (batch_size, sequence_length).
		    inputs_embeds (tp.Optional[chex.Array]): Input embeddings. Shape: (batch_size, sequence_length, hidden_size).
		        Either `input_ids` or `inputs_embeds` must be provided.
		    attention_mask (tp.Optional[chex.Array]): Mask to avoid performing attention on padding token indices.
		        Shape: (batch_size, sequence_length).
		    position_ids (tp.Optional[chex.Array]): Position indices for the tokens.
		        Shape: (batch_size, sequence_length).
		    segment_ids (tp.Optional[chex.Array]): Segment IDs (unused).
		    output_attentions (tp.Optional[bool]): Whether to return attention weights. Defaults to `config.output_attentions`.
		    output_hidden_states (tp.Optional[bool]): Whether to return hidden states for all layers.
		        Defaults to `config.output_hidden_states`.
		    past_key_values (tp.Optional[TransformerCache | PagedAttentionCache]): Precomputed key/value states for attention.
		    cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
		    return_dict (bool): Whether to return a `CausalLMOutput` object or a tuple.

		Returns:
		    tp.Union[CausalLMOutput, tp.Tuple]: The model's output. If `return_dict` is True,
		        returns a `CausalLMOutput` object containing `logits`, `hidden_states` (optional),
		        and `attentions` (optional). Otherwise, returns a tuple with these elements.
		"""
		outputs = self.model(
			input_ids=input_ids,
			attention_mask=attention_mask,
			position_ids=position_ids,
			output_attentions=output_attentions,
			output_hidden_states=output_hidden_states,
			past_key_values=past_key_values,
			cache_metadata=cache_metadata,
			return_dict=return_dict,
			inputs_embeds=inputs_embeds,
			segment_ids=segment_ids,
		)

		hidden_states = outputs[0]

		if self.config.tie_word_embeddings:
			lm_logits = jax.lax.dot_general(
				hidden_states,
				self.model.tok_embeddings.embedding.value.T,
				(((hidden_states.ndim - 1), (0,)), ((), ())),
			)
		else:
			lm_logits = self.output(hidden_states)

		if not return_dict:
			return (lm_logits,) + outputs[1:]

		return CausalLMOutput(
			logits=lm_logits,
			hidden_states=outputs.hidden_states,
			attentions=outputs.attentions,
			past_key_values=outputs.past_key_values,
		)


@register_module(
	TaskType.SEQUENCE_CLASSIFICATION,
	config=InternLM2Config,
	model_type="internlm2",
)
class InternLM2ForSequenceClassification(EasyDeLBaseModule):
	"""InternLM2 model with a Sequence Classification head.

	This model consists of the base InternLM2 transformer (`InternLM2Model`) followed by a
	linear layer (`score`) that projects the transformer's output hidden states
	(typically the hidden state of the first token) to the number of classes for classification.

	Attributes:
	    config (InternLM2Config): Configuration object for the model.
	    dtype (jnp.dtype): Data type for computation. Default is jnp.float32.
	    param_dtype (jnp.dtype): Data type for parameters. Default is jnp.float32.
	    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Default is None.
	    rngs (nn.Rngs): Random number generators.
	    module (InternLM2Model): The core InternLM2 transformer model.
	    score (ParallelLinear): The linear layer for classification.
	"""

	def __init__(
		self,
		config: InternLM2Config,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	):
		"""Initializes the InternLM2ForSequenceClassification model.

		Args:
		    config (InternLM2Config): The configuration object for the InternLM2 model.
		    dtype (jnp.dtype): Data type for computation. Defaults to jnp.float32.
		    param_dtype (jnp.dtype): Data type for parameters. Defaults to jnp.float32.
		    precision (jax.lax.PrecisionLike): Precision setting for JAX operations. Defaults to None.
		    rngs (nn.Rngs): Random number generators.
		"""
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.model = InternLM2Model(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		assert hasattr(config, "num_labels"), (
			"in order to use `SequenceClassification` Models in `EasyDeL` you first need to attach `num_labels` to model `config`"
		)
		self.score = ParallelLinear(
			self.config.hidden_size,
			config.num_labels,
			dtype=dtype,
			param_dtype=param_dtype,
			use_bias=False,
			kernel_init=jax.nn.initializers.normal(stddev=config.initializer_range),
			precision=self.precision,
			rngs=rngs,
		)

	def __call__(
		self,
		input_ids: tp.Optional[chex.Array] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		past_key_values: tp.Optional[TransformerCache | PagedAttentionCache] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		output_attentions: tp.Optional[bool] = None,
		output_hidden_states: tp.Optional[bool] = None,
		return_dict: bool = True,
	) -> tp.Union[SequenceClassifierOutput, tp.Tuple]:
		"""Forward pass of the InternLM2ForSequenceClassification model.

		Args:
		    input_ids (tp.Optional[chex.Array]): Input token IDs. Shape: (batch_size, sequence_length).
		    inputs_embeds (tp.Optional[chex.Array]): Input embeddings. Shape: (batch_size, sequence_length, hidden_size).
		        Either `input_ids` or `inputs_embeds` must be provided.
		    attention_mask (tp.Optional[chex.Array]): Mask to avoid performing attention on padding token indices.
		        Shape: (batch_size, sequence_length).
		    position_ids (tp.Optional[chex.Array]): Position indices for the tokens.
		        Shape: (batch_size, sequence_length).
		    segment_ids (tp.Optional[chex.Array]): Segment IDs (unused).
		    past_key_values (tp.Optional[TransformerCache | PagedAttentionCache]): Precomputed key/value states for attention.
		    cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata]): Metadata for paged attention.
		    output_attentions (tp.Optional[bool]): Whether to return attention weights. Defaults to `config.output_attentions`.
		    output_hidden_states (tp.Optional[bool]): Whether to return hidden states for all layers.
		        Defaults to `config.output_hidden_states`.
		    return_dict (bool): Whether to return a `SequenceClassifierOutput` object or a tuple.

		Returns:
		    tp.Union[SequenceClassifierOutput, tp.Tuple]: The model's output. If `return_dict` is True,
		        returns a `SequenceClassifierOutput` object containing `logits`, `hidden_states` (optional),
		        and `attentions` (optional). Otherwise, returns a tuple with these elements.
		"""
		transformer_outputs = self.model(
			input_ids=input_ids,
			attention_mask=attention_mask,
			position_ids=position_ids,
			past_key_values=past_key_values,
			cache_metadata=cache_metadata,
			output_attentions=output_attentions,
			output_hidden_states=output_hidden_states,
			return_dict=return_dict,
			inputs_embeds=inputs_embeds,
			segment_ids=segment_ids,
		)

		hidden_states = transformer_outputs[0]
		logits = self.score(hidden_states)
		if input_ids is not None:
			batch_size = input_ids.shape[0]
		else:
			batch_size = inputs_embeds.shape[0]

		if self.config.pad_token_id is None and batch_size != 1:
			raise ValueError("Cannot handle batch sizes > 1 if no padding token is defined.")
		if self.config.pad_token_id is None:
			sequence_lengths = -1
		else:
			if input_ids is not None:
				sequence_lengths = (
					jnp.argmax(jnp.equal(input_ids, self.config.pad_token_id).astype("i4"), -1)
					- 1
				)
				sequence_lengths = sequence_lengths % input_ids.shape[-1]
			else:
				sequence_lengths = -1

		pooled_logits = logits[jnp.arange(batch_size), sequence_lengths]

		if not return_dict:
			output = (pooled_logits,) + transformer_outputs[1:]
			return output

		return SequenceClassifierOutput(
			logits=pooled_logits,
			past_key_values=past_key_values,
			hidden_states=transformer_outputs.hidden_states,
			attentions=transformer_outputs.attentions,
		)
