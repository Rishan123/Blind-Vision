import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers

# Helper libraries
import numpy as np
import PIL.Image as Image
import matplotlib.pylab as plt

# Download the model from :https://tfhub.dev/google/imagenet/inception_resnet_v2/classification/4
classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"

# Load the image of a lobster. You can change this to your own image. It does not expect a PNG image.
img = 'C:/Users/alosha01/Downloads/OpenCV 4.1.2/opencv/samples/data/apple.jpg'

# Resize the image
shape = (224, 224)
img = Image.open(img).resize(shape)

# Convert the image to a NumPy array.
img = np.array(img)/255.0

# Get the labels, and turn it into a NumPy array.
labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
labels = np.array(open(labels_path).read().splitlines())

# Make the Sequential model
model = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=shape+(3,),trainable=True) 
])

prediction_array = model.predict(img[np.newaxis, ...])
prediction = np.argmax(prediction_array[0], axis=-1) # Find the top predicted class.

plt.imshow(img)
plt.axis('off')

prediction = labels[prediction] # Show the prediction and image using matplotlib.
plt.title("Prediction: " + prediction.title())
plt.show()