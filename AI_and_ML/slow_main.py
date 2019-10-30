import tensorflow as tf
import tensorflow_hub as hub

# Helper libraries
import numpy as np
import PIL.Image as Image
from picamera import PiCamera
import RPi.GPIO as GPIO
from gtts import gTTS
import os

camera = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setup(2,GPIO.IN)

# Download the model from :https://tfhub.dev/google/imagenet/inception_resnet_v2/classification/4
classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/4"
shape = (224, 224)
# Get the labels, and turn it into a NumPy array.
labels_path = '/home/pi/tf/labels.txt'
labels = np.array(open(labels_path).read().splitlines())

# Make the Sequential model
model = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=shape+(3,),trainable=True) 
])
language = 'en'
print('Ready')
while True:
    if GPIO.input(2):
        camera.capture('/home/pi/cap.jpg')
        img = '/home/pi/cap.jpg'
        # Resize the image
        img = Image.open(img).resize(shape)

        # Convert the image to a NumPy array.
        img = np.array(img)/255.0

        prediction_array = model.predict(img[np.newaxis, ...])
        prediction = np.argmax(prediction_array[0], axis=-1) # Find the top predicted class.

        prediction = labels[prediction] # Show the prediction and image using matplotlib.
        text = str(prediction.title())
        sp = gTTS(text=text, lang=language, slow=False)
        sp.save('/home/pi/tf/prediction.mp3')
        os.system('omxplayer /home/pi/tf/prediction.mp3')
        print('Ready')

