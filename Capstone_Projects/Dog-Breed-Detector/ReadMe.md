[//]: # (Image References)

[image1]: ./dog_images3/American_water_spaniel_00648.jpg "Output1"
[image2]: ./dog_images3/Brittany_02625.jpg "Output2"
[image3]: ./dog_images3/Curly-coated_retriever_03896.jpg "Output3"
[image4]: ./dog_images3/Boykin_spaniel_02501.jpg "Output11"
[image5]: ./dog_images3/Smooth_fox_terrier_08094.jpg "Output22"
[image6]: ./dog_images3/Curly-coated_retriever_03902.jpg "Output33"

[image7]: ./human_images3/octavia.jpg "Output4"
[image8]: ./human_images3/sotomayor.jpg "Output5"
[image9]: ./human_images3/sravanth.jpg "Output6"
[image10]: ./human_images3/Pharaoh_hound_07722.jpg "Output44"
[image11]: ./human_images3/Chinese_crested_03500.jpg "Output55"
[image12]: ./human_images3/Cocker_spaniel_03744.jpg "Output66"


# Overview/Summary:
The goal of the project is to develope an algorithm that can accept any user-supplied image as input. If a dog is detected in the image, it will provide an estimate of the dog's breed. If a human is detected, it will provide an estimate of the dog breed that is most resembling. The final results looked like below:

- Dog Breed 'Curley Coated Retriever' was identified as 'Curley Coated Retriever'
    ### ![Output3][image3] 
    ('Curley Coated Retriever') 
    ### ![Output33][image6] 
    ('Curley Coated Retriever')

- Dog Breed 'American water spaniel' was identified as 'Boykin spaniel'
    ### ![Output1][image1]
    ('American water spaniel')  
    ### ![Output11][image4]
    ('Boykin spaniel')

- Dog Breed 'Britanny' was identified as 'Smooth fox terrier'
    ### ![Output2][image2]  
    ('Britanny')
    ### ![Output22][image5]
    ('Smooth fox terrier')


- Person 'Octavia' was identified as 'Pharaoh hound'.
    ### ![Output4][image7]  
    ('Octavia')
    ### ![Output44][image10]
    ('Pharaoh hound')

- Person 'Sotomayor' was identified as 'Chinese crested'.
    ### ![Output5][image8]  
    ('Sotomayor')
    ### ![Output55][image11]
    ('Chinese crested')

- Person 'Sai Sravanth' was identified as 'Cocker spaniel'.
    ### ![Output6][image9] 
    ('Sai Sravanth')
    ### ![Output66][image12]
    ('Cocker spaniel')


# Architecture:
- ### With Convolutional Neural Network (CNN) from scratch:

        ## Define layers of a CNN
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.conv4 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv5 = nn.Conv2d(128, 256, 3, padding=1)
        
        self.maxpool = nn.MaxPool2d(2,2)
        
        ## 128*16*16
        self.fc1 = nn.Linear(64*32*32, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 256)
        self.fc4 = nn.Linear(256, 133)
        
        self.dropout = nn.Dropout(0.05)
        
        self.batchNormal1 = nn.BatchNorm2d(16)
        self.batchNormal2 = nn.BatchNorm2d(32)
        self.batchNormal3 = nn.BatchNorm2d(64)


- ### Using VGG16 model with "Transfer-Learning":
        ## Define layers of a CNN
        VGG16(
        (features): Sequential(
            (0): Conv2d(3, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (1): ReLU(inplace)
            (2): Conv2d(64, 64, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (3): ReLU(inplace)
            (4): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            (5): Conv2d(64, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (6): ReLU(inplace)
            (7): Conv2d(128, 128, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (8): ReLU(inplace)
            (9): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            (10): Conv2d(128, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (11): ReLU(inplace)
            (12): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (13): ReLU(inplace)
            (14): Conv2d(256, 256, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (15): ReLU(inplace)
            (16): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            (17): Conv2d(256, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (18): ReLU(inplace)
            (19): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (20): ReLU(inplace)
            (21): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (22): ReLU(inplace)
            (23): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
            (24): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (25): ReLU(inplace)
            (26): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (27): ReLU(inplace)
            (28): Conv2d(512, 512, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1))
            (29): ReLU(inplace)
            (30): MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False)
        )
        (classifier): Sequential(
            (0): Linear(in_features=25088, out_features=4096, bias=True)
            (1): ReLU(inplace)
            (2): Dropout(p=0.5)
            (3): Linear(in_features=4096, out_features=4096, bias=True)
            (4): ReLU(inplace)
            (5): Dropout(p=0.5)
            (6): Linear(in_features=4096, out_features=133, bias=True)
        )
        )

# Data Preprocessing:
### With Convolutional Neural Network (CNN) from scratch):
- Applied RandomResizCrop() on input images as the input size of images is different for different dog breeds. The random resize applied is 256x256.
- All input images are normalized with a mean of (0.485, 0.456, 0.406) and a standard deveation of (0.229, 0.224, 0.225). 
- All input images are converted to tensor type.

### Using VGG16 model with "Transfer-Learning":
- All input images are resized to 224x224.
- Images are randomly rotated in range (-30, +30) degress.
- Images are randomly flipped (vertically) with a probability of 50%.
- All input images are normalized with a mean of (0.485, 0.456, 0.406) and a standard deveation of (0.229, 0.224, 0.225). 
- All input images are converted to tensor type.


# Loss Function & Hyperparameters:
1. With Convolutional Neural Network (CNN) from scratch):
    - learning rate = 0.01
    - momentum=0.9
    - Epochs = 25
    - criterion = Cross Entropy Loss
    - optimizer = Stochastic Gradient Descent
2. Using VGG16 model with "Transfer-Learning":
    - learning rate = 0.00025
    - momentum=0.9
    - Epochs = 100
    - criterion = Cross Entropy Loss
    - optimizer = Stochastic Gradient Descent

# Results:
1. With Convolutional Neural Network (CNN) from scratch): **Test Accuracy: 14% (122/836)**
2. Using VGG16 model with "Transfer-Learning": 
    **Test Accuracy: 76% (637/836)**

Possible improvements:
- Changing the model from VGG to RESNET/Inception might improve performance
- Supplying the model with a lot more dog images per breed.
- Adjusting the learn rate based on number of epochs, like using any technique from 'torch.optim.lr_scheduler'


# Code:
https://github.com/saisravanth/udacity/blob/master/Capstone_Projects/Dog-Breed-Detector/dog_app.ipynb


# References
1. https://pytorch.org/docs/stable/torchvision/transforms.html
2. https://pytorch.org/docs/stable/optim.html 
3. https://pytorch.org/docs/master/data.html#torch.utils.data.DataLoader
4. https://pytorch.org/docs/stable/torchvision/datasets.html
5. http://www.image-net.org/
6. https://docs.opencv.org/master/d7/d8b/tutorial_py_face_detection.html
7. https://pytorch.org/docs/stable/nn.html#loss-functions
8. https://medium.com/@Biboswan98/optim-adam-vs-optim-sgd-lets-dive-in-8dbf1890fbdc

