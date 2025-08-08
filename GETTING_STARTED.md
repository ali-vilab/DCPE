## Getting Started
### Requirements
- Linux with Python ≥ 3.7
- PyTorch ≥ 2.1
- A100 GPUs

Before running the following commands, make sure Python can locate the project modules.
You can either run `export PYTHONPATH=$(pwd)` once in your terminal, or prepend `PYTHONPATH=$(pwd)` to each command.


### Pre-extract discrete codes of training images
```
bash scripts/autoregressive/extract_codes_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --data-path /path/to/imagenet/train --code-path /path/to/imagenet_code_c2i_flip_ten_crop --ten-crop --crop-range 1.1 --image-size 256
```
and/or
``` 
bash scripts/autoregressive/extract_codes_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --data-path /path/to/imagenet/train --code-path /path/to/imagenet_code_c2i_flip_ten_crop_105 --ten-crop --crop-range 1.05 --image-size 256
```


### Train AR models with DDP, using DCPE
Before running, please change `nnodes, nproc_per_node, node_rank, master_addr, master_port` in `.sh`.
```
bash scripts/autoregressive/train_c2i.sh --code-path /path/to/imagenet_code_c2i_flip_ten_crop --image-size 256 --gpt-model GPT-B --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --codebook-compression --codebook-compression-rate 2

bash scripts/autoregressive/train_c2i.sh --code-path /path/to/imagenet_code_c2i_flip_ten_crop --image-size 256 --gpt-model GPT-L --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --codebook-compression --codebook-compression-rate 2

bash scripts/autoregressive/train_c2i.sh --code-path /path/to/imagenet_code_c2i_flip_ten_crop --image-size 256 --gpt-model GPT-XL --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --codebook-compression --codebook-compression-rate 2
```
Set `--resume-time` when needed.


### Train refine models
```
bash scripts/autoregressive/train_refine_net.sh --code-path /path/to/imagenet_code_c2i_flip_ten_crop --idx-to-cluster path/to/idx_to_cluster.pt --in-vocab-size 8192
```
Set `--idx-to-cluster` to the `idx_to_cluster.pt` obtained in the last step.


### Sampling
```
bash scripts/autoregressive/sample_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --gpt-ckpt path/to/gpt_ckpt.pt --gpt-model GPT-B --image-size 256 --image-size-eval 256 --cfg-scale 2.0 --codebook-compression --codebook-compression-rate 2

bash scripts/autoregressive/sample_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --gpt-ckpt path/to/gpt_ckpt.pt --gpt-model GPT-L --image-size 256 --image-size-eval 256 --cfg-scale 1.85 --codebook-compression --codebook-compression-rate 2

bash scripts/autoregressive/sample_c2i.sh --vq-ckpt ./pretrained_models/vq_ds16_c2i.pt --gpt-ckpt path/to/gpt_ckpt.pt --gpt-model GPT-XL --image-size 256 --image-size-eval 256 --cfg-scale 1.85 --codebook-compression --codebook-compression-rate 2
```
Specify `--gpt-ckpt` to downloaded checkpoint like `./pretrained_models/DCPE-B/DCPE-B.pt`, or checkpoint in training folder.

To use refine model, specify `--refine-net-path` and `--refine-net-layers`.


### Evaluation
Before evaluation, please refer [evaluation readme](evaluations/c2i/README.md) to install required packages. 
```
python evaluations/c2i/evaluator.py evaluations/c2i/VIRTUAL_imagenet256_labeled.npz samples/{XXXXX}-size-384-size-256-VQ-16-topk-0-topp-1.0-temperature-1.0-cfg-2.0-seed-0.npz
```