#import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# Load the CIFAR10 dataset. CIFAR10 is a small dataset with only 10 classes. Strangely, when you train CIFAR10 with the
# neural network, it gives a 4 dimensional output. To try this out, change 'mnist' to cifar10. Then run the model.
cifar = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = cifar.load_data()

# Scale the RGB values to ranges of 0 and 1. It is very important you do it to the training set and the testing set.
train_images = train_images / 255.0
test_images = test_images / 255.0

# Because the class names are not defined in the dataset, we need to provide ourselves.
class_names = ['airplane','automobile','cat','deer','dog','frog','horse','ship','truck']

# Create the layers. Layers extract representations from the data fed into them.
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)), # Transform the format of the images from 2D to 1D. Think of this layer
    # as unstacking rows of pixels in the image and lining them up.
    keras.layers.Dense(128, activation='relu'), # These Dense layers are fully connected neural layers. This layer has 128
    # nodes (or neurons).
    keras.layers.Dense(10, activation='softmax') # This layer is a 10 node 'softmax' layer that returns an array of 10
    # probability scores that sum to 1. Each node contains a score that indicates the probability that the current image
    # belongs to one of the 10 classes.
])

# Compile the model. Before the model is trained, it needs a few more settings:
model.compile(optimizer='adam', # This is how the model is updated based on the data it sees and its loss function.
              loss='sparse_categorical_crossentropy', # This measure how well the model is doing during training.
              metrics=['accuracy']) # Used to monitor the training and testing steps. The following example uses accuracy,
              # the fraction of the images that are correctly classified.

# Training the neural network requires the following steps:

# Feed the data into the model. It's like how you eat food, if you eat it and you like it, you start eating more.

# The model learns to associate images and labels.

# You ask the model to make predictions about a test set—in this example, the test_images array. Verify that the
# predictions match the labels from the test_labels array.


model.fit(train_images, train_labels, epochs=2)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2) # Evaluate the model and assign 'test_loss' and
# 'test_acc' to it.

# Print the accuracy and the training loss
print('\nTest accuracy:', int(test_acc*100),'%')
print('\nTest loss:',int(test_loss))