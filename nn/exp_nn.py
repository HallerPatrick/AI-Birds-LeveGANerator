#!/usr/bin/env python3s
# coding: utf-8

import os
# PIL for opening,resizing and saving images
from PIL import Image
# tqdm for a progress bar when loading the dataset
from tqdm import tqdm
import numpy as np


from keras.layers import Input, Reshape, Dropout, Dense, Flatten, BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model, load_model
from keras.optimizers import Adam


# Sample image(s) with following specs:
# PNG image data, 842 x 482, 8-bit/color RGB, non-interlaced
img = "samples"
IMAGE_SHAPE = (842, 482, 3)
random_noise_dimension = 100


# Build discriminator
# Discriminator attempts to classify real and generated images

model = Sequential()
model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=(512, 256, 3), padding="same"))

# Leaky relu is similar to usual relu. If x < 0 then f(x) = x * alpha, otherwise f(x) = x.
model.add(LeakyReLU(alpha=0.2))
# Dropout blocks some connections randomly. This help the model to generalize better.
# 0.25 means that every connection has a 25% chance of being blocked.
model.add(Dropout(0.25))
model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
# Zero padding adds additional rows and columns to the image. Those rows and columns are made of zeros.
model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
model.add(BatchNormalization(momentum=0.8))
model.add(LeakyReLU(alpha=0.2))

model.add(Dropout(0.25))
model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
model.add(BatchNormalization(momentum=0.8))
model.add(LeakyReLU(alpha=0.2))

model.add(Dropout(0.25))
model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
model.add(BatchNormalization(momentum=0.8))
model.add(LeakyReLU(alpha=0.2))

model.add(Dropout(0.25))
model.add(Conv2D(512, kernel_size=3, strides=1, padding="same"))
model.add(BatchNormalization(momentum=0.8))
model.add(LeakyReLU(alpha=0.2))

model.add(Dropout(0.25))
# Flatten layer flattens the output of the previous layer to a single dimension.
model.add(Flatten())
# Outputs a value between 0 and 1 that predicts whether image is real or generated. 0 = generated, 1 = real.
model.add(Dense(1, activation='sigmoid'))

model.summary()

input_image = Input(shape=IMAGE_SHAPE)

# Model output given an image.
validity = model(input_image)

discriminator = Model(input_image, validity)
optimizer = Adam(0.0002, 0.5)
discriminator.compile(loss="binary_crossentropy", optimizer=optimizer)

# Build generator

model = Sequential()

model.add(Dense(512*8*8, activation="relu",
                input_dim=random_noise_dimension))
model.add(Reshape((8, 8, 512)))

# Four layers of upsampling, convolution, batch normalization and activation.
# 1. Upsampling: Input data is repeated. Default is (2,2). In that case a 4x4x256 array becomes an 8x8x256 array.
# 2. Convolution: If you are not familiar, you should watch this video: https://www.youtube.com/watch?v=FTr3n7uBIuE
# 3. Normalization normalizes outputs from convolution.
# 4. Relu activation:  f(x) = max(0,x). If x < 0, then f(x) = 0.

model.add(UpSampling2D())
model.add(Conv2D(256, kernel_size=3, padding="same"))
model.add(BatchNormalization(momentum=0.8))
model.add(Activation("relu"))

model.add(UpSampling2D())
model.add(Conv2D(256, kernel_size=3, padding="same"))
model.add(BatchNormalization(momentum=0.8))
model.add(Activation("relu"))

model.add(UpSampling2D((4, 2)))
# model.add(Conv2D(128, kernel_size=3, padding="same"))
# model.add(BatchNormalization(momentum=0.8))
# model.add(Activation("relu"))

model.add(UpSampling2D((2, 2)))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(128, kernel_size=3, padding="same"))
model.add(BatchNormalization(momentum=0.8))
model.add(Activation("relu"))

#model.add(Reshape((421, 241, 64)))

# Last convolutional layer outputs as many featuremaps as channels in the final image.
model.add(Conv2D(3, kernel_size=3, padding="same"))
# tanh maps everything to a range between -1 and 1.
model.add(Activation("tanh"))

# show the summary of the model architecture
model.summary()

# Placeholder for the random noise input
input = Input(shape=(random_noise_dimension,))
# Model output
generated_image = model(input)

# Change the model type from Sequential to Model (functional API) More at: https://keras.io/models/model/.
generator = Model(input, generated_image)


random_input = Input(shape=(random_noise_dimension,))

generated_image = generator(random_input)
discriminator.trainable = False

validity = discriminator(generated_image)

combined = Model(random_input, validity)
combined.compile(loss="binary_crossentropy", optimizer=optimizer)



def get_training_data(datafolder):
    print("Loading training data...")

    training_data = []
    # Finds all files in datafolder
    filenames = os.listdir(datafolder)
    for filename in tqdm(filenames):
        # Combines folder name and file name.
        path = os.path.join(datafolder, filename)
        # Opens an image as an Image object.
        image = Image.open(path)
        # Resizes to a desired size.
        image = image.resize(
            (IMAGE_SHAPE[0], IMAGE_SHAPE[1]), Image.ANTIALIAS)
        # Creates an array of pixel values from the image.
        pixel_array = np.asarray(image)

        training_data.append(pixel_array)


    # training_data is converted to a numpy array
    training_data = np.reshape(training_data, (-1, *IMAGE_SHAPE))
    return training_data


training_data = get_training_data(img)
training_data = training_data / 127.5 - 1.

# Two arrays of labels. Labels for real images: [1,1,1 ... 1,1,1], labels for generated images: [0,0,0 ... 0,0,0]
labels_for_real_images = np.ones((32, 1))
labels_for_generated_images = np.zeros((32, 1))
    

for epoch in range(2):
    # Select a random half of images
    indices = np.random.randint(0, training_data.shape[0], 32)
    real_images = training_data[indices]

    
    # Generate random noise for a whole batch.
    random_noise = np.random.normal(
        0, 1, (32, random_noise_dimension))
    # Generate a batch of new images.
    
    generated_images = generator.predict(random_noise)
    
    # Train the discriminator on real images.
    discriminator_loss_real = discriminator.train_on_batch(
        real_images, labels_for_real_images)
    # Train the discriminator on generated images.
    discriminator_loss_generated = discriminator.train_on_batch(
        generated_images, labels_for_generated_images)
    # Calculate the average discriminator loss.
    discriminator_loss = 0.5 *         np.add(discriminator_loss_real, discriminator_loss_generated)

    # Train the generator using the combined model. Generator tries to trick discriminator into mistaking generated images as real.
    generator_loss = combined.train_on_batch(
        random_noise, labels_for_real_images)
    print("%d [Discriminator loss: %f, acc.: %.2f%%] [Generator loss: %f]" % (
        epoch, discriminator_loss[0], 100*discriminator_loss[1], generator_loss))

    if epoch % save_images_interval == 0:
        save_images(epoch)



