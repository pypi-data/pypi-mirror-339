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
from flax import nnx as nn
from jax import numpy as jnp

from easydel.infra.base_module import EasyDeLBaseModule
from easydel.infra.factory import TaskType, register_module
from easydel.infra.modeling_outputs import BaseModelOutput, CausalLMOutput
from easydel.infra.utils import (
	ACT2FN,
	auto_remat,
	control_mlp_sharding,
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

from .gpt_neox_configuration import GPTNeoXConfig as GPTNeoXConfig


class GPTNeoXAttention(AttentionModule):
	"""GPT-NeoX Attention module.

	This module implements the attention mechanism used in the GPT-NeoX model,
	including rotary position embeddings and parallel linear layers for QKV.

	Attributes:
		config (GPTNeoXConfig): Configuration object for the model.
		dtype (jnp.dtype): Data type for computations.
		param_dtype (jnp.dtype): Data type for parameters.
		precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
		rngs (nn.Rngs): Random number generators.
	"""

	def __init__(
		self,
		config: GPTNeoXConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	) -> None:
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		self.rngs = rngs
		self.head_dim = self.config.hidden_size // self.config.num_attention_heads
		self.rotary = self.config.get_basic_rope(
			dtype=dtype,
			head_size=self.head_dim,
			rotary_dim=int(self.head_dim * self.config.rotary_pct),
			base=self.config.rotary_emb_base,
		)
		self.query_key_value = ParallelLinear(
			config.hidden_size,
			3 * config.hidden_size,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.dense = ParallelLinear(
			config.hidden_size,
			config.hidden_size,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.attention_performer = FlexibleAttentionModule(
			base_config=config,
			softmax_scale=self.head_dim**-0.5,
			dropout_prob=config.attention_dropout,
		)

	def _split_heads(self, hidden_states):
		return hidden_states.reshape(
			hidden_states.shape[:2] + (self.config.num_attention_heads, self.head_dim)
		)

	def __call__(
		self,
		hidden_states: chex.Array,
		attention_mask: chex.Array,
		position_ids: chex.Array,
		causal_mask: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		cache_view: tp.Optional[TransformerCacheView | PagedAttentionCacheView] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		output_attentions: bool = False,
		frequencies: tp.Optional[chex.Array] = None,
	):
		"""Forward pass of the GPTNeoXAttention module.

		Args:
		    hidden_states (chex.Array): Input hidden states.
		    attention_mask (chex.Array): Mask to apply on the attention scores.
		    position_ids (chex.Array): Position indices for the tokens.
		    causal_mask (chex.Array, optional): Causal mask for ensuring autoregressive behavior.
		    segment_ids (tp.Optional[chex.Array], optional): Segment IDs for segment-based attention.
		    cache_view (tp.Optional[TransformerCacheView | PagedAttentionCacheView], optional): Cache view for key/value states.
		    cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata], optional): Metadata for cache handling.
		    output_attentions (bool, optional): Whether to return attention weights.
		    frequencies (tp.Optional[chex.Array], optional): Precomputed rotary frequencies.

		Returns:
		    tp.Tuple[chex.Array, tp.Optional[chex.Array]]: A tuple containing the attention output and optionally the attention weights.
		"""
		query, key, value = jnp.split(
			self.query_key_value(hidden_states),
			indices_or_sections=3,
			axis=-1,
		)

		query = self._split_heads(query)
		key = self._split_heads(key)
		value = self._split_heads(value)
		query, key = self.rotary(
			positions=position_ids,
			query=query,
			key=key,
			frequencies=frequencies,
		)

		(
			key,
			value,
			attention_mask,
			init_attention_bias,
		) = self.concatenate(
			query=query,
			key=key,
			cache_view=cache_view,
			value=value,
			attention_mask=attention_mask,
			causal_mask=causal_mask,
			fcm_mask=None,
		)

		attentions = self.attention_performer.forward(
			query_states=query,
			key_states=key,
			value_states=value,
			bias=None,
			cache_metadata=cache_metadata,
			cache_view=cache_view,
			init_bias=init_attention_bias,
			attention_mask=attention_mask,
			segment_ids=segment_ids,
			causal=True,
			dropout_rng=self.rngs.params(),
		)

		attn_output = self.shard_attention_prod(
			self._merge_heads(attentions.attention_outputs)
		)
		attn_output = self.dense(attn_output)
		return attn_output, attentions.attention_weights


class GPTNeoXMlp(nn.Module):
	"""GPT-NeoX MLP module.

	This module implements the feed-forward network used in the GPT-NeoX model.

	Attributes:
		config (GPTNeoXConfig): Configuration object for the model.
		dtype (jnp.dtype): Data type for computations.
		param_dtype (jnp.dtype): Data type for parameters.
		precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
		rngs (nn.Rngs): Random number generators.
	"""

	def __init__(
		self,
		config: GPTNeoXConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	) -> None:
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		self.dense_h_to_4h = ParallelLinear(
			self.config.hidden_size,
			self.config.intermediate_size,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.dense_4h_to_h = ParallelLinear(
			self.config.intermediate_size,
			self.config.hidden_size,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.act = ACT2FN[self.config.hidden_act]

	def __call__(self, hidden_states):
		"""Forward pass of the GPTNeoXMlp module.

		Args:
		    hidden_states (chex.Array): Input hidden states.

		Returns:
		    chex.Array: Output hidden states after processing through the MLP.
		"""
		hidden_states = control_mlp_sharding(
			hidden_states,
			self.config.partition_axis,
		)
		return self.dense_4h_to_h(self.act(self.dense_h_to_4h(hidden_states)))


class GPTNeoXBlock(nn.Module):
	"""GPT-NeoX Transformer block.

	This module represents a single transformer block in the GPT-NeoX model,
	containing self-attention and MLP sub-layers with residual connections
	and layer normalization. It supports both standard and parallel residual connections.

	Attributes:
		config (GPTNeoXConfig): Configuration object for the model.
		dtype (jnp.dtype): Data type for computations.
		param_dtype (jnp.dtype): Data type for parameters.
		precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
		rngs (nn.Rngs): Random number generators.
	"""

	def __init__(
		self,
		config: GPTNeoXConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: jax.lax.PrecisionLike = None,
		*,
		rngs: nn.Rngs,
	) -> None:
		self.config = config
		self.dtype = dtype
		self.param_dtype = param_dtype
		self.precision = precision
		self.rngs = rngs
		self.use_parallel_residual = config.use_parallel_residual

		attn_block = GPTNeoXAttention
		mlp_block = GPTNeoXMlp

		attn_block, mlp_block = auto_remat(
			attn_block,
			mlp_block,
			policy=config.gradient_checkpointing,
		)
		self.input_layernorm = nn.LayerNorm(
			config.hidden_size,
			epsilon=config.layer_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		self.post_attention_layernorm = nn.LayerNorm(
			config.hidden_size,
			epsilon=config.layer_norm_eps,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		self.attention = GPTNeoXAttention(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.mlp = GPTNeoXMlp(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)

	def __call__(
		self,
		hidden_states: chex.Array,
		attention_mask: chex.Array,
		position_ids: chex.Array,
		causal_mask: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		cache_view: tp.Optional[TransformerCacheView | PagedAttentionCacheView] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		output_attentions: bool = False,
		frequencies: tp.Optional[chex.Array] = None,
	):
		"""Forward pass of the GPTNeoXBlock module.

		Args:
		    hidden_states (chex.Array): Input hidden states.
		    attention_mask (chex.Array): Mask to apply on the attention scores.
		    position_ids (chex.Array): Position indices for the tokens.
		    causal_mask (chex.Array, optional): Causal mask for ensuring autoregressive behavior.
		    segment_ids (tp.Optional[chex.Array], optional): Segment IDs for segment-based attention.
		    cache_view (tp.Optional[TransformerCacheView | PagedAttentionCacheView], optional): Cache view for key/value states.
		    cache_metadata (tp.Optional[TransformerMetadata | PagedAttentionMetadata], optional): Metadata for cache handling.
		    output_attentions (bool, optional): Whether to return attention weights.
		    frequencies (tp.Optional[chex.Array], optional): Precomputed rotary frequencies.

		Returns:
		    tp.Tuple[chex.Array, tp.Optional[chex.Array]]: A tuple containing the output hidden states and optionally the attention weights.
		"""
		attn_out = self.attention(
			self.input_layernorm(hidden_states),
			attention_mask,
			position_ids,
			causal_mask,
			segment_ids,
			cache_view,
			cache_metadata,
			output_attentions,
			frequencies,
		)
		attn = attn_out[0]
		if self.use_parallel_residual:
			mlp = self.mlp(self.post_attention_layernorm(hidden_states))
			hidden_states = mlp + hidden_states + attn
		else:
			hidden_states = attn + hidden_states
			hidden_states = (
				self.mlp(self.post_attention_layernorm(hidden_states)) + hidden_states
			)
		return (hidden_states,) + attn_out[1:]


@register_module(
	TaskType.BASE_MODULE,
	config=GPTNeoXConfig,
	model_type="gpt_neox",
)
class GPTNeoXModel(EasyDeLBaseModule):
	"""GPT-NeoX model implementation.

	This class implements the main GPT-NeoX transformer model architecture, consisting of
	an embedding layer, multiple GPTNeoXBlock layers, and a final layer normalization.

	Attributes:
		config (GPTNeoXConfig): Configuration object for the model.
		dtype (jnp.dtype): Data type for computations.
		param_dtype (jnp.dtype): Data type for parameters.
		precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
		rngs (nn.Rngs): Random number generators.
	"""

	def __init__(
		self,
		config: GPTNeoXConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: tp.Optional[tp.Union[str, jax.lax.Precision]] = None,
		*,
		rngs: nn.Rngs,
	):
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.embed_in = nn.Embed(
			self.config.vocab_size,
			self.config.hidden_size,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)
		self.emb_dropout = nn.Dropout(config.hidden_dropout, rngs=rngs)
		self.layers = [
			GPTNeoXBlock(
				config=config,
				dtype=dtype,
				param_dtype=param_dtype,
				precision=precision,
				rngs=rngs,
			)
			for i in range(config.num_hidden_layers)
		]
		self.final_layer_norm = nn.LayerNorm(
			config.hidden_size,
			epsilon=self.config.layer_norm_eps,
			dtype=self.dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)

	@functools.cached_property
	def frequencies(self):
		head_dim = self.config.hidden_size // self.config.num_attention_heads
		return self.config.get_basic_frequencies(
			head_size=head_dim,
			rotary_dim=int(head_dim * self.config.rotary_pct),
			base=self.config.rotary_emb_base,
		)

	def __call__(
		self,
		input_ids: tp.Optional[chex.Array] = None,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		past_key_values: tp.Optional[TransformerCache | PagedAttentionCache] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		extra_embedding: tp.Optional[chex.Array] = None,
		output_attentions: bool = False,
		output_hidden_states: bool = False,
		return_dict: bool = True,
	):
		"""Forward pass through the GPTNeoXModel.

		Args:
		    input_ids (chex.Array, optional): Input token IDs, shape (batch_size, sequence_length).
		    attention_mask (chex.Array, optional): Mask to avoid attention on padding tokens.
		    position_ids (chex.Array, optional): Indices of positions of each input sequence token.
		    past_key_values (TransformerCache | PagedAttentionCache, optional): Cache containing precomputed key/value states.
		    cache_metadata (TransformerMetadata | PagedAttentionMetadata, optional): Metadata for cache handling.
		    inputs_embeds (chex.Array, optional): Input embeddings, shape (batch_size, sequence_length, hidden_size).
		    segment_ids (chex.Array, optional): Segment token indices for segment embeddings.
		    extra_embedding (chex.Array, optional): Additional embedding to add to input embeddings.
		    output_attentions (bool, optional): Whether to return attention weights.
		    output_hidden_states (bool, optional): Whether to return hidden states of all layers.
		    return_dict (bool, optional): Whether to return a model output object or a tuple.

		Returns:
		    Union[BaseModelOutput, Tuple]: Model outputs (last hidden state, optional hidden states, optional attentions)
		"""
		all_attentions = () if output_attentions else None
		all_hidden_states = () if output_hidden_states else None
		if (input_ids is None) ^ (inputs_embeds is not None):
			raise ValueError(
				"You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
			)
		if inputs_embeds is None:
			inputs_embeds = self.embed_in(input_ids.astype("i4"))

		batch_size, sequence_length, _ = inputs_embeds.shape
		if attention_mask is None:
			attention_mask = jnp.ones((batch_size, sequence_length), "b1")
		else:
			if attention_mask.dtype != jnp.bool:
				attention_mask = jnp.astype(attention_mask == 1, "b1")
		if position_ids is None:
			position_ids = jnp.broadcast_to(
				jnp.clip(jnp.cumsum(attention_mask, axis=-1) - 1, a_min=0),
				(batch_size, sequence_length),
			).astype(jnp.int32)

		assert sequence_length <= self.config.max_position_embeddings, (
			f"Maximum Position Embedding Reached ! (Excepted <= {self.config.max_position_embeddings} got {sequence_length})"
		)

		hidden_states = self.emb_dropout(
			inputs_embeds + extra_embedding if extra_embedding is not None else inputs_embeds
		)

		if past_key_values is None:
			past_key_values = TransformerCache.init_empty(len(self.layers))

		for idx, block in enumerate(self.layers):
			if output_hidden_states:
				all_hidden_states += (hidden_states,)
			hidden_states, attn_weight = block(
				hidden_states=hidden_states,
				attention_mask=attention_mask,
				position_ids=position_ids,
				cache_view=past_key_values.views[idx],
				cache_metadata=cache_metadata,
				segment_ids=segment_ids,
				causal_mask=self.causal_mask,
				frequencies=self.frequencies,
				output_attentions=output_attentions,
			)
			if output_attentions:
				all_attentions += (attn_weight,)
		hidden_states = self.final_layer_norm(hidden_states)
		if output_hidden_states:
			all_hidden_states += (hidden_states,)

		outputs = (
			hidden_states,
			all_hidden_states,
			all_attentions,
		)
		if return_dict:
			return BaseModelOutput(
				last_hidden_state=hidden_states,
				hidden_states=outputs[1],
				attentions=outputs[2],
			)

		return tuple([v for v in outputs if v is not None])


@register_module(
	TaskType.CAUSAL_LM,
	config=GPTNeoXConfig,
	model_type="gpt_neox",
)
class GPTNeoXForCausalLM(EasyDeLBaseModule):
	"""GPT-NeoX model with a language modeling head.

	This model extends the base GPTNeoXModel by adding a linear layer on top to
	predict the next token in a sequence, making it suitable for causal language
	modeling tasks.

	Attributes:
		config (GPTNeoXConfig): Configuration object for the model.
		dtype (jnp.dtype): Data type for computations.
		param_dtype (jnp.dtype): Data type for parameters.
		precision (jax.lax.PrecisionLike): Precision setting for JAX operations.
		rngs (nn.Rngs): Random number generators.
	"""

	def __init__(
		self,
		config: GPTNeoXConfig,
		dtype: jnp.dtype = jnp.float32,
		param_dtype: jnp.dtype = jnp.float32,
		precision: tp.Optional[tp.Union[str, jax.lax.Precision]] = None,
		*,
		rngs: nn.Rngs,
	):
		super().__init__(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.gpt_neox = GPTNeoXModel(
			config=config,
			dtype=dtype,
			param_dtype=param_dtype,
			precision=precision,
			rngs=rngs,
		)
		self.lm_head = ParallelLinear(
			config.hidden_size,
			config.vocab_size,
			use_bias=False,
			dtype=dtype,
			param_dtype=param_dtype,
			rngs=rngs,
		)

	def __call__(
		self,
		input_ids,
		attention_mask: tp.Optional[chex.Array] = None,
		position_ids: tp.Optional[chex.Array] = None,
		past_key_values: tp.Optional[TransformerCache | PagedAttentionCache] = None,
		cache_metadata: tp.Optional[TransformerMetadata | PagedAttentionMetadata] = None,
		inputs_embeds: tp.Optional[chex.Array] = None,
		segment_ids: tp.Optional[chex.Array] = None,
		extra_embedding: tp.Optional[chex.Array] = None,
		output_attentions: bool = False,
		output_hidden_states: bool = False,
		return_dict: bool = True,
	):
		"""Forward pass through the GPTNeoXForCausalLM model.

		Args:
		    input_ids (chex.Array, optional): Input token IDs, shape (batch_size, sequence_length).
		    attention_mask (chex.Array, optional): Mask to avoid attention on padding tokens.
		    position_ids (chex.Array, optional): Indices of positions of each input sequence token.
		    past_key_values (TransformerCache | PagedAttentionCache, optional): Cache containing precomputed key/value states.
		    cache_metadata (TransformerMetadata | PagedAttentionMetadata, optional): Metadata for cache handling.
		    inputs_embeds (chex.Array, optional): Input embeddings, shape (batch_size, sequence_length, hidden_size).
		    segment_ids (chex.Array, optional): Segment token indices for segment embeddings.
		    extra_embedding (chex.Array, optional): Additional embedding to add to input embeddings.
		    output_attentions (bool, optional): Whether to return attention weights.
		    output_hidden_states (bool, optional): Whether to return hidden states of all layers.
		    return_dict (bool, optional): Whether to return a model output object or a tuple.

		Returns:
		    Union[CausalLMOutput, Tuple]: Model outputs (logits, optional hidden states, optional attentions)
		"""
		outputs = self.gpt_neox(
			input_ids=input_ids,
			attention_mask=attention_mask,
			position_ids=position_ids,
			past_key_values=past_key_values,
			cache_metadata=cache_metadata,
			inputs_embeds=inputs_embeds,
			segment_ids=segment_ids,
			extra_embedding=extra_embedding,
			output_attentions=output_attentions,
			output_hidden_states=output_hidden_states,
			return_dict=return_dict,
		)
		hidden_states = outputs[0]

		if self.config.tie_word_embeddings:
			lm_logits = jax.lax.dot_general(
				hidden_states,
				self.gpt_neox.embed_in.embedding.value.T,
				(((hidden_states.ndim - 1), (0,)), ((), ())),
			)
		else:
			lm_logits = self.lm_head(hidden_states)

		lm_logits = lm_logits.astype(jnp.float32)

		if not return_dict:
			return (lm_logits,) + outputs[1:]

		return CausalLMOutput(
			logits=lm_logits,
			hidden_states=outputs.hidden_states,
			attentions=outputs.attentions,
			past_key_values=outputs.past_key_values,
		)
