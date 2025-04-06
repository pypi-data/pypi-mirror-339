# Copyright 2024 The AI Edge Torch Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Utility functions for externalized KV Cache."""

import dataclasses
from typing import List, Tuple

from ai_edge_torch.generative.custom_ops.dynamic_update_slice import dynamic_update_slice
from ai_edge_torch.generative.layers import model_config
import torch
import torch.utils._pytree as pytree


@dataclasses.dataclass
class KVCacheEntry:
  """A single cache entry that includes K and V caches.

  The chaches are built based on the provided config with the shape of
  (batch_size=1, kv_cache_max, num_query_groups, head_dim).
  """

  k_cache: torch.Tensor
  v_cache: torch.Tensor

  @classmethod
  def from_model_config(
      cls,
      kv_cache_max: int,
      config: model_config.AttentionConfig,
      dtype: torch.dtype = torch.float32,
      device: torch.device = None,
      batch_size: int = 1,
  ) -> "KVCacheEntry":
    """Build an instance of the class based on model config."""
    shape = (batch_size, kv_cache_max, config.num_query_groups, config.head_dim)
    k = torch.zeros(shape, dtype=dtype, device=device)
    v = torch.zeros(shape, dtype=dtype, device=device)
    obj = cls(k_cache=k, v_cache=v)
    return obj


@dataclasses.dataclass
class KVCache:
  """A utility class for holding KV cache entries per layer."""

  caches: Tuple[KVCacheEntry, ...]

  @classmethod
  def from_model_config(
      cls,
      config: model_config.ModelConfig,
      dtype: torch.dtype = torch.float32,
      device: torch.device = None,
      batch_size: int = 1,
  ) -> "KVCache":
    """Build an instance of the class based on model config.

    Args:
        config (ModelConfig): Model config used for building the cache.
        dtype (torch.dtype, optional): The data type of the cache tensor.
          Defaults to torch.float32.
        device (torch.device, optional): The device placement of the cache
          tensors. Defaults to None.
        batch_size (int, optional): The batch size of the cache tensors.
          Defaults to 1.

    Returns:
        KVCache: The created cache object.
    """
    caches = [
        KVCacheEntry.from_model_config(
            config.kv_cache_max
            if not config.block_config(idx).kv_cache_max_len
            else config.block_config(idx).kv_cache_max_len,
            config.block_config(idx).attn_config,
            dtype,
            device,
            batch_size,
        )
        for idx in range(config.num_layers)
    ]
    obj = cls(caches=tuple(caches))
    return obj

  def flatten(self) -> List[torch.Tensor]:
    """Flatten the cache entries into a list of tensors with order k_i, v_i."""
    flattened, _ = _flatten_kvc(self)
    return flattened


def _flatten_kvc(kvc: KVCache) -> Tuple[List[str], List[str]]:
  flattened = []
  flat_names = []
  none_names = []
  for i, kv_entry in enumerate(kvc.caches):
    flattened.append(kv_entry.k_cache)
    flat_names.append(f"k_{i}")
    flattened.append(kv_entry.v_cache)
    flat_names.append(f"v_{i}")
  return flattened, [flat_names, none_names]


def _flatten_kvc_with_keys(kvc: KVCache) -> Tuple[List, List]:
  flattened, (flat_names, none_names) = _flatten_kvc(kvc)
  return [
      (pytree.MappingKey(k), v) for k, v in zip(flat_names, flattened)
  ], flat_names


def _unflatten_kvc(
    values: List[torch.Tensor], context: Tuple[List, List]
) -> KVCache:
  assert len(values) % 2 == 0, "Found odd number of K and V entries."
  num_layers = len(values) // 2
  flat_names = context[0]
  kv_entries = []
  for i in range(num_layers):
    k_cache_idx = flat_names.index(f"k_{i}")
    v_cache_idx = flat_names.index(f"v_{i}")
    kv_entries.append(
        KVCacheEntry(k_cache=values[k_cache_idx], v_cache=values[v_cache_idx])
    )
  obj = KVCache(tuple(kv_entries))
  return obj


pytree.register_pytree_node(
    KVCache,
    _flatten_kvc,
    _unflatten_kvc,
    flatten_with_keys_fn=_flatten_kvc_with_keys,
    serialized_type_name="",
)


def update(
    cache: KVCacheEntry,
    input_pos: torch.Tensor,
    k_slice: torch.Tensor,
    v_slice: torch.Tensor,
    use_dus: bool = True,
) -> KVCacheEntry:
  """Out of place update of Cache buffer.

  Args:
      cache (KVCacheEntry): The original cache buffer.
      input_pos (torch.Tensor): The update slice positions.
      k_slice (torch.Tensor): The K slice to be updated in the new cache.
      v_slice (torch.Tensor): The V slice to be updated in the new cache.

  Returns:
      KVCacheEntry: The updated KVCache entry based on the passed inputs.
  """
  update_kv_cache = _update_kv_impl if use_dus else _update_kv_base_impl
  return update_kv_cache(cache, input_pos, k_slice, v_slice)


def _update_kv_base_impl(
    cache: KVCacheEntry,
    input_pos: torch.Tensor,
    k_slice: torch.Tensor,
    v_slice: torch.Tensor,
) -> KVCacheEntry:
  """Update the cache buffer without High Level Function Boundary annotation."""
  k = cache.k_cache.index_copy(1, input_pos.to(torch.long), k_slice)
  v = cache.v_cache.index_copy(1, input_pos.to(torch.long), v_slice)
  updated_cache = KVCacheEntry(k, v)
  return updated_cache


def _get_slice_indices(positions: torch.Tensor) -> torch.Tensor:
  """Dynamic Update Slice updates are a variadic sequence of 0-rank tensors."""

  zero = torch.zeros([]).int()
  positions = positions.int()[0].reshape([])
  return [zero, positions, zero, zero]


def _update_kv_impl(
    cache: KVCacheEntry,
    input_pos: torch.Tensor,
    k_slice: torch.Tensor,
    v_slice: torch.Tensor,
) -> KVCacheEntry:
  """Update the cache buffer for K and V caches."""
  # NB: Here assume that input_pos == range(input_pos[0], len(input_pos))

  k_slice_indices = _get_slice_indices(input_pos)
  v_slice_indices = _get_slice_indices(input_pos)

  k = dynamic_update_slice(cache.k_cache, k_slice, k_slice_indices)
  v = dynamic_update_slice(cache.v_cache, v_slice, v_slice_indices)

  updated_cache = KVCacheEntry(k, v)
  return updated_cache
