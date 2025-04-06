################################################################################
## GENERATED FILE INFO
##
## Template Source: training/python/split_embedding_codegen_lookup_invoker.template
################################################################################

#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-ignore-all-errors

import torch
from .lookup_args import *
def invoke(
    common_args: CommonArgs,
    optimizer_args: OptimizerArgs,
    total_unique_indices: int,
    iter: int = 0,
    apply_global_weight_decay: bool = False,
    # only pass prev_iter_dev since prev_iter is never created on UVM
    prev_iter_dev: Optional[torch.Tensor] = None,
    gwd_lower_bound: float = 0.0,
) -> torch.Tensor:

    vbe_metadata = common_args.vbe_metadata

    return torch.ops.fbgemm.split_embedding_codegen_lookup_none_function(
        # common_args
        placeholder_autograd_tensor=common_args.placeholder_autograd_tensor,
        dev_weights=common_args.dev_weights,
        uvm_weights=common_args.uvm_weights,
        lxu_cache_weights=common_args.lxu_cache_weights,
        weights_placements=common_args.weights_placements,
        weights_offsets=common_args.weights_offsets,
        D_offsets=common_args.D_offsets,
        total_D=common_args.total_D,
        max_D=common_args.max_D,
        hash_size_cumsum=common_args.hash_size_cumsum,
        total_hash_size_bits=common_args.total_hash_size_bits,
        indices=common_args.indices,
        offsets=common_args.offsets,
        pooling_mode=common_args.pooling_mode,
        indice_weights=common_args.indice_weights,
        feature_requires_grad=common_args.feature_requires_grad,
        lxu_cache_locations=common_args.lxu_cache_locations,
        uvm_cache_stats=common_args.uvm_cache_stats,
        # VBE metadata
        B_offsets=vbe_metadata.B_offsets,
        vbe_output_offsets_feature_rank=vbe_metadata.output_offsets_feature_rank,
        vbe_B_offsets_rank_per_feature=vbe_metadata.B_offsets_rank_per_feature,
        max_B=vbe_metadata.max_B,
        max_B_feature_rank=vbe_metadata.max_B_feature_rank,
        vbe_output_size=vbe_metadata.output_size,
        # optimizer_args
        total_hash_size = optimizer_args.total_hash_size, # if optimizer == none
        # momentum1
        # momentum2
        # prev_iter
        
        prev_iter_dev=prev_iter_dev,
        # row_counter
        # iter
        iter=iter,
        # max counter
        # total_unique_indices
        total_unique_indices = total_unique_indices,
        output_dtype=common_args.output_dtype,
        is_experimental=common_args.is_experimental,
        use_uniq_cache_locations_bwd=common_args.use_uniq_cache_locations_bwd,
        use_homogeneous_placements=common_args.use_homogeneous_placements,
        apply_global_weight_decay=apply_global_weight_decay,
        gwd_lower_bound=gwd_lower_bound,
    )