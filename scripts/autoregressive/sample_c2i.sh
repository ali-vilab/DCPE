# !/bin/bash
set -x

gpu_count=$(nvidia-smi --list-gpus | wc -l)

torchrun \
--nnodes=1 --nproc_per_node=$gpu_count --node_rank=0 \
--master_port=12345 \
autoregressive/sample/sample_c2i_ddp.py \
"$@"
