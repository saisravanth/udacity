import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets

from PIL import Image
from PIL import ImageFile 

import json
from datetime import datetime


class Utility:
    
    def get_transforms(self):
        
        transform = transforms.Compose([
        transforms.RandomResizedCrop(size=(224)),
        transforms.RandomRotation(degrees=30),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
        ])

        transform_basic = transforms.Compose([
        transforms.RandomResizedCrop(size=(224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),(0.229, 0.224, 0.225))
        ])
        
        return transform, transform_basic 
    
    def get_dataLoaders(self, transform, transform_basic, data_dir='flowers'):
        
        train_dir = data_dir + '/train'
        valid_dir = data_dir + '/valid'
        test_dir = data_dir + '/test'
    
        train_data = datasets.ImageFolder(train_dir, transform=transform)
        data_loader_train = torch.utils.data.DataLoader(train_data,
                                                  batch_size=32,
                                                  shuffle=True      
                                                  )

        test_data = datasets.ImageFolder(test_dir, transform=transform_basic)
        data_loader_test = torch.utils.data.DataLoader(test_data,
                                                  batch_size=32,
                                                  shuffle=True
                                                  )

        validation_data = datasets.ImageFolder(valid_dir, transform=transform_basic)
        data_loader_valid = torch.utils.data.DataLoader(validation_data,
                                                  batch_size=32,
                                                  shuffle=True
                                                  )


        loaders_transfer = {'train': data_loader_train, 'test': data_loader_test, 'valid':data_loader_valid}
        
        return loaders_transfer
    
    def get_cat_to_name(self):
        with open('cat_to_name.json', 'r') as f:
            cat_to_name = json.load(f)
        return cat_to_name    
    
#     def move_to_GPU(self, model, data):
#         if use_cuda:
#             model = model.cuda()
#             data = data.cuda()
#             print("Data and model moved to GPU !!")
#             return model, data
#         else:
#             print("Running on CPU...")
#             return model, data
            
    
    
        