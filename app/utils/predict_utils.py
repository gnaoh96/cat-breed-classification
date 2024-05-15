import base64
import copy
import os
import random
import re
import shutil
import sys
import time
from glob import glob

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from PIL import Image

os.environ["CUDA_LAUNCH_BLOCKING"] = "0"


# Define device
def define_device():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    return device


# Load model state function
def load_model_state(model, path, device):
    model.load_state_dict(torch.load(path, map_location=torch.device(device)))
    model = model.to(device)
    return model


# Define transform
def transform_img():
    ### Transform image
    # the expected normalization by the pretrained model
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )

    # transforms for the images (without augmentation)
    # here, both train and test have the same transformation
    image_transforms = {
        # 'train': transforms.Compose([
        #     transforms.Resize(size=256),
        #     transforms.CenterCrop(size=224),
        #     transforms.ToTensor(),
        #     normalize
        # ]),
        "test": transforms.Compose(
            [
                transforms.Resize(size=256),
                transforms.CenterCrop(size=224),
                transforms.ToTensor(),
                normalize,
            ]
        )
    }

    # transforms with augmentation on the training data
    augmented_image_transforms = {
        # 'train': transforms.Compose([
        #     transforms.Resize(size=256),
        #     transforms.CenterCrop(size=224),
        #     transforms.RandomHorizontalFlip(),
        #     transforms.ColorJitter(brightness=0.2, contrast=0.2),
        #     transforms.ToTensor(),
        #     normalize
        # ]),
        "test": transforms.Compose(
            [
                transforms.Resize(size=256),
                transforms.CenterCrop(size=224),
                transforms.ToTensor(),
                normalize,
            ]
        )
    }

    # train and test directory paths
    # train_directory = 'data/train'
    test_directory = "data/test"

    # load data from folders
    data = {
        # 'train': datasets.ImageFolder(root=train_directory), # transforms applied in the cross validation later
        "test": datasets.ImageFolder(
            root=test_directory, transform=image_transforms["test"]
        )
    }

    # mapping class index to class name
    idx_to_class = {val: key for key, val in data["test"].class_to_idx.items()}
    return image_transforms, augmented_image_transforms, idx_to_class


# Load model to inference
def load_model(device):
    ### Save model to inference
    # get the pretrained resnet50
    resnet50 = torchvision.models.resnet50(weights="ResNet50_Weights.IMAGENET1K_V1")

    # freeze model parameters
    for param in resnet50.parameters():
        param.requires_grad = False

    # change the final layer of ResNet50 model for transfer learning
    fc_inputs = resnet50.fc.in_features
    resnet50.fc = nn.Sequential(
        nn.Linear(fc_inputs, 12), nn.LogSoftmax(dim=1)  # For using NLLLoss()
    )

    # load the model state
    resnet50 = load_model_state(
        resnet50, "model/resnet50-model-augmentation.pth", device
    )

    return resnet50


# Predict function
### Predict function
def predict(model, img, k, device, transform_type, idx_to_class):  # , actual_label):
    """display an image along with the top k predictions"""
    predict_image = None
    try:
        img.verify()  # verify img is an image (not string of path)
        predict_image = img
    except Exception:
        predict_image = Image.open(img)

    # open and transform the image
    transform = transform_type["test"]

    predict_image_tensor = transform(predict_image)
    predict_image_tensor = predict_image_tensor.view(1, 3, 224, 224)
    predict_image_tensor = predict_image_tensor.to(device)

    with torch.no_grad():
        model.eval()
        out = model(predict_image_tensor)
        ps = torch.exp(out)

        # get the topk result
        topprob, topclass = ps.topk(k, dim=1)
        topprob_np = topprob.cpu().numpy()[0]
        topclass_np = topclass.cpu().numpy()[0]

        # print the prediction result
        # print('Actual :')
        # print('-',actual_label,'\n')
        print("Top", k, "prediction :")
        for idx, prob in enumerate(topprob_np):
            print("-", idx_to_class[topclass_np[idx]], ":", f"{prob*100:.2f}%")

        # display the image
        # plt.figure()
        # plt.imshow(predict_image)
        # plt.show()
        print("------------------------------------------------------")
