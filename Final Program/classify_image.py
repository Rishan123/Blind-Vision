# Load libraries 
import matplotlib.pylab as plt
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import PIL.Image as Image

# Download the Mobilenet classifier from this link: 
classifier_url ="https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"

IMAGE_SHAPE = (224, 224)

# Create the model #
model = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
])

img = '/home/pi/tf/cat.jpeg'
img = Image.open(img).resize(IMAGE_SHAPE)


# Convert the image to a Numpy array. 
img = np.array(img)/255.0

# Predict the image using the classifier
result = model.predict(img[np.newaxis, ...])

# Find the top predicted class
predicted_class = np.argmax(result[0], axis=-1)

# Fetch the ImageNet labels, and decode the predictions
labels_path = tf.keras.utils.get_file('ImageNetLabels.txt','https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = np.array(open(labels_path).read().splitlines())

# Show the image with the title of the prediction.
plt.imshow(img)
plt.axis('off')
predicted_class_name = imagenet_labels[predicted_class]
_ = plt.title("Prediction: " + predicted_class_name.title())
plt.show()
