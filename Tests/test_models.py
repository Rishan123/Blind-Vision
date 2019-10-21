import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# Load the CIFAR10 dataset. CIFAR10 is a small dataset with only 10 classes. Strangely, when you train CIFAR10 with the
# neural network, it gives a 4 dimensional output. To try this out, change 'mnist' to cifar10. Then run the model.
mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Scale the RGB values to ranges of 0 and 1. It is very important you do it to the training set and the testing set.
train_images = train_images / 255.0
test_images = test_images / 255.0

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

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


model.fit(train_images, train_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2) # Evaluate the model and assign 'test_loss' and
# 'test_acc' to it.

# Print the accuracy and the training loss
print('\nTest accuracy:', int(test_acc*100),'%')
print('\nTest loss:',int(test_loss*100),'%')

predictions = model.predict(test_images) # Predict the test mages and assign predictions to it.

def predict_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array, true_label[i], img[i] #

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array) # Returns the indices of the maximum values along an axis.
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color) # Plot on matplotib
    
    print("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label])) # Print

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
i = num_images
predict_image(i, predictions[i], test_labels, test_images) # Call the function
plt.show()
