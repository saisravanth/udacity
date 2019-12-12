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


class Model:
    
    def createModel(self, model_name, use_cuda):
        
        if torch.cuda.is_available() and use_cuda:
            device = torch.device("cuda")
            print("Device selected as GPU inside createModel !!")
        else:
            device = torch.device("cpu")
            print("Device selected as CPU inside createModel")
    
        if model_name == "VGG16":
            model_transfer = models.vgg16(pretrained=True)
            
            for param in model_transfer.features.parameters():
                param.require_grad = False
                
            model_transfer.classifier[6] = nn.Linear(4096, 102)
            return model_transfer.to(device) 
        
        if model_name == "VGG19":
            model_transfer = models.vgg19(pretrained=True)
            
            for param in model_transfer.features.parameters():
                param.require_grad = False
                
            model_transfer.classifier[6] = nn.Linear(4096, 102)
            return model_transfer.to(device)      
    
    
    def get_criterion_optimizer(self, model_transfer, learnRate=0.00025, momentum=0.9):
        criterion_transfer = nn.CrossEntropyLoss()
        optimizer_transfer = optim.SGD(model_transfer.classifier.parameters(), lr=learnRate, momentum=momentum)
        
        return criterion_transfer, optimizer_transfer
    
    
    def train(self, n_epochs, loaders, model, arch, optimizer, criterion, use_cuda, save_path):
        """returns trained model"""
        # initialize tracker for minimum validation loss
        valid_loss_min = np.Inf 
        bestEpoch = []
        
        if torch.cuda.is_available() and use_cuda:
            device = torch.device("cuda")
            print("Device selected as GPU !!")
        else:
            device = torch.device("cpu")
            print("Device selected as CPU")
    
        for epoch in range(1, n_epochs+1):
            # initialize variables to monitor training and validation loss
            train_loss = 0.0
            valid_loss = 0.0

            ###################
            # train the model #
            ###################
            model.train()
            for batch_idx, (data, target) in enumerate(loaders['train']):
                # move to GPU
                if torch.cuda.is_available() and use_cuda:
                    data, target = data.to(device), target.to(device)
                # Set gradients to 0
                optimizer.zero_grad()
                # Get output
                output = model(data)               
                # Calculate loss
                loss = criterion(output, target)
                train_loss += loss.item() * data.size(0)
                # Calculate gradients
                loss.backward()
                # Take step
                optimizer.step()
            train_loss = train_loss/len(loaders['train'].dataset)

            ######################    
            # validate the model #
            ######################
            model.eval()
            for batch_idx, (data, target) in enumerate(loaders['valid']):
                # move to GPU
                if use_cuda:
                    data, target = data.cuda(), target.cuda()
                ## update the average validation loss
                outputs = model(data)
                loss = criterion(outputs, target)
                valid_loss += loss.item() * data.size(0)
            valid_loss = valid_loss/len(loaders['test'].dataset)

            # print training/validation statistics 
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")

            print('Epoch: {} \tTime: {} \tTraining Loss: {:.6f} \tValidation Loss: {:.6f}'.format(
                epoch, 
                dt_string,
                train_loss,
                valid_loss
                ))

            ## TODO: save the model if validation loss has decreased
            if valid_loss <= valid_loss_min:
                print('Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...'.format(
                valid_loss_min,
                valid_loss))
                
                if arch == 'VGG16':
                    torch.save({'architecture': 'VGG16', 
                                'class_to_idx': loaders['train'].dataset.class_to_idx, 
                                'state_dict': model.state_dict()}, save_path)
                
                if arch == 'VGG19':
                    torch.save({'architecture': 'VGG19', 
                                'class_to_idx': loaders['train'].dataset.class_to_idx, 
                                'state_dict': model.state_dict()}, save_path)
                
        
                valid_loss_min = valid_loss 
                bestEpoch.append(epoch)


            # If the model doesn't save in 5 consecutive epoches, break the loop
            if epoch-bestEpoch[-1] >= 5:
                break

        # return trained model
        return model
    
    
    def load_model(self, checkpoint, use_cuda):
        
        checkpoint = torch.load(checkpoint)
        if checkpoint['architecture'] == "VGG16":
            model = models.vgg16(pretrained=True)
            for param in model.features.parameters():
                param.require_grad = False
            model.classifier[6] = nn.Linear(4096, 102)
            model.class_to_idx = checkpoint['class_to_idx']
            model.load_state_dict(checkpoint['state_dict'])
            if use_cuda:
                model = model.cuda()
            return model    
        elif checkpoint['architecture'] == "VGG19":
            model = models.vgg19(pretrained=True)
            for param in model.features.parameters():
                param.require_grad = False
            model.classifier[6] = nn.Linear(4096, 102)
            model.class_to_idx = checkpoint['class_to_idx']
            model.load_state_dict(checkpoint['state_dict'])
            if use_cuda:
                model = model.cuda()
            return model       
        else:
            print("Model must be VGG16 or VGG19 to load a checkpoint")
            return None 

    
    def process_image(self, image_path):
    
        # TODO: Process a PIL image for use in a PyTorch model
        image = Image.open(image_path)
        print("Original image: ", image.size)
        if image.size[0] > image.size[1]:
            image.thumbnail((10000,256))
        else:    
            image.thumbnail((256,10000))
        print("after thumbnail: ", image.size)

        width = image.width
        height = image.height
        new_width = 224
        new_height = 224

        left = (width - new_width)/2   
        top = (height - new_height)/2
        right = (width + new_width)/2
        bottom = (height + new_height)/2

        image = image.crop((left, top, right, bottom))

        #Normalize the image
        image = np.array(image)
        print("after cropping: ",image.shape)
        image = image/255
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]

        image = (image-mean)/std
        image = image.transpose((2,0,1))
        print("after normalization and transpose: ", image.shape)
        print(type(image))

        return image
        
    
    def predict(self, image_path, model, use_cuda, topk=5):
    
        # TODO: Implement the code to predict the class from an image file
        image = self.process_image(image_path)
        image = torch.torch.Tensor(image)
        image = image.unsqueeze_(0)                                              # makes a mini-batch of size 1
        print("before prediction, image size: ", image.shape)

        if use_cuda:
                image = image.cuda()
                model = model.cuda()   

        output = model(image)
        output = output.view(102)
        print("output shape: ", output.shape)
        print("output type: ", type(output))

        probs, indeces = torch.topk(output, topk)
        probs = probs.squeeze().tolist()                                          
        
        class_to_idx = model.class_to_idx
        idx_to_class = {v: k for k, v in class_to_idx.items()} 
        print(indeces)
        classes = [idx_to_class[i] for i in indeces.squeeze().tolist()]           
        
        return probs, classes
    
    
    
    
    
    