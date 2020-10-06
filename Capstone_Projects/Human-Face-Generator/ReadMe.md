[//]: # (Image References)

[image1]: ./assets/processed_face_data_64x64_.png "Output1"
[image2]: ./assets/processed_face_data_32x32_.png "Output2"
[image3]: ./assets/32x32_final_result_.png "Output3"
[image4]: ./assets/TrainingLoss_.png "Output4"


# Project Overview:
The goal of the project is to define and train a **Deep Convolutional Generative Adversarial Network (DCGAN)** on a dataset of faces and finally have a **generator network** that can create new images of faces that the network has never seen before. 

The final results from the **generator network** are fairly realistic faces with small amounts of noise as seen below.

### ![Output3][image3] 


# Architecture:
- #### A **Deep Convolutional Generative Adversarial Network (DCGAN)** is comprised of two adversarial networks, a discriminator and a generator.
- #### A discriminator is a combination of **Convolutional layers with batch normalization layers** (this excludes maxpooling layers) and a final fully connected layer. 
- #### A generator is a combination of a fully connected layer coupled with **Transpose Convolution layers and batch normalization layers**


        Discriminator(
        (conv1): Sequential(
            (0): Conv2d(3, 64, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
        )
        (conv2): Sequential(
            (0): Conv2d(64, 128, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
            (1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (conv3): Sequential(
            (0): Conv2d(128, 256, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
            (1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (fc): Linear(in_features=4096, out_features=1, bias=True)
        )

        Generator(
        (fc): Linear(in_features=100, out_features=4096, bias=True)
        (t_conv1): Sequential(
            (0): ConvTranspose2d(1024, 256, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
            (1): BatchNorm2d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (t_conv2): Sequential(
            (0): ConvTranspose2d(256, 128, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
            (1): BatchNorm2d(128, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (t_conv3): Sequential(
            (0): ConvTranspose2d(128, 64, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
            (1): BatchNorm2d(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
        )
        (t_conv4): Sequential(
            (0): ConvTranspose2d(64, 3, kernel_size=(4, 4), stride=(2, 2), padding=(1, 1), bias=False)
        )
        )



# Data Preprocessing:
- Data used was **CelebA** that has more than 200K celebrity images.Each of the **CelebA** image has been cropped to remove parts of the image that don't include a face, then resized down to 64x64x3 NumPy images. Final total number of images include only 89,931.
- Each of these images was further reduced to 32x32x3. Resizing the data to a smaller size would make for faster training, while still creating convincing images of faces!
- The 64x64 input and the 32x32 input images looked as below: 
    ### ![Output1][image1]
    (64x64)
    ### ![Output2][image2]
    (32x32)
     
- Each pixel value of the image is re-scaled such that its initial range was changed from (0, 1) to (-1, +1).
- All input images are converted to tensor type.


# Loss Function & Hyperparameters:
1. Generator and Discriminator:
    - learning rate = 0.0002
    - beta1 = 0.5, beta2 = 0.999 (coefficients used for computing running averages of gradient and its square)
    - z_size = 100    (The length of the input latent vector, z)
    - d_conv_dim = 64 (The depth of the first convolutional layer)
    - g_conv_dim = 64 (The depth of the inputs to the *last* transpose convolutional layer)
    - Epochs = 50
    - criterion = BCEWithLogitsLoss  (binary cross entropy with logits loss)
    - optimizer = Adam

2. For the discriminator, the total loss is the sum of the losses for real and fake images, d_loss = d_real_loss + d_fake_loss. We want the discriminator to output 1 for real images and 0 for fake images.

3. The generator loss will look similar only with flipped labels. The generator's goal is to get the discriminator to think its generated images are real.

4. Training:
    - Discriminator is trained by alternating on real and fake images.
    - Generator learns by trying to trick the discriminator. **Both have opposing loss function.**
5. All weights were initialized from a zero-centered Normal distribution with standard deviation 0.02. This was done for only convolutional and linear layers as suggest in the original DCGAN paper.


# Results:
- The Generator does make fake images that resemble human faces !! However, from the plotted graph, it is evident that Generator couldn't convince the Discriminator entirely with the fake images.
    ### ![Output4][image4]  

Possible improvements:
- To improve above, the generator needs to have few more parameters(a deeper network) added to it to help it learn better. A deeper Discriminator and also a much deeper Generator can definitely make the netowrk produce better results.
- Using **Implicit Competitive Regularization** (ICR) in GANs and retraining the model.


# Code:
https://github.com/saisravanth/udacity/blob/master/Capstone_Projects/Human-Face-Generator/dlnd_face_generation.ipynb


# References
1. https://arxiv.org/pdf/1511.06434.pdf
2. http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html
3. https://pytorch.org/docs/stable/torchvision/datasets.html#imagefolder
4. https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix/blob/master/models/networks.py
5. https://arxiv.org/abs/1412.6980
6. https://arxiv.org/abs/1711.05101
7. https://pytorch.org/docs/stable/torchvision/transforms.html
8. https://en.wikipedia.org/wiki/Channel_(digital_image)#RGB_Images
9. https://pytorch.org/docs/stable/optim.html 
10. https://pytorch.org/docs/master/data.html#torch.utils.data.DataLoader
11. https://pytorch.org/docs/stable/nn.html#loss-functions
12. https://arxiv.org/abs/1910.05852