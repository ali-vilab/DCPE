import torch
import numpy as np
import os
from torch.utils.data import Dataset
from torchvision.datasets import ImageFolder
from PIL import Image
import json


class CustomDataset(Dataset):
    def __init__(self, data_path, transform):
        with open(data_path, "r") as f:
            paths = json.load(f)
        self.samples = paths
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, target = self.samples[idx]
        with open(path, "rb") as f:
            img = Image.open(f).convert("RGB")
        if self.transform is not None:
            img = self.transform(img)

        return img, target


def build_imagenet_val(args, transform):
    return CustomDataset(args.data_path, transform=transform)
