# !/bin/bash
set -x

nnodes=1
nproc_per_node=$(nvidia-smi --list-gpus | wc -l)
node_rank=0
master_addr=localhost
master_port=42424

torchrun \
--nnodes=$nnodes --nproc_per_node=$nproc_per_node --node_rank=$node_rank \
--master_addr=$master_addr --master_port=$master_port \
autoregressive/train/train_refine_net.py "$@"
