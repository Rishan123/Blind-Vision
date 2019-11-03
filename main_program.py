import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers

# Helper libraries
import numpy as np
import PIL.Image as Image
from picamera import PiCamera
#import RPi.GPIO as GPIO
from gpiozero import Button
from gtts import gTTS
import os

camera = PiCamera()
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(15,GPIO.IN)
button = Button(15,pull_up=False)

classifier_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/classification/2"
shape = (224, 224)
# Get the labels, and turn it into a NumPy array.
#labels_path = '/home/pi/tf/ImageNetLabels.txt'
#labels = np.array(open(labels_path).read().splitlines())

speech_labels = '/home/pi/tf/labels.txt'
speech_labels = np.array(open(speech_labels).read().splitlines())

# Make the Sequential model
model = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=shape+(3,)) 
])
language = 'en'
text = 'Ready'
sp = gTTS(text=text, lang=language, slow=False)
sp.save('/home/pi/tf/ready.mp3')
os.system('omxplayer /home/pi/tf/ready.mp3')
print('Ready')
try:
    while True:
        #if GPIO.input(15):
        button.wait_for_press()
        camera.capture('/home/pi/cap.jpg')
        img = '/home/pi/cap.jpg'
        # Resize the image
        img = Image.open(img).resize(shape)

        # Convert the image to a NumPy array.
        img = np.array(img)/255.0

        prediction_array = model.predict(img[np.newaxis, ...])
        prediction = np.argmax(prediction_array[0], axis=-1) # Find the top predicted class.

        #plt.imshow(img)
        #plt.axis('off')

        #prediction = labels[prediction] # Show the prediction and image using matplotlib.
        speech = speech_labels[prediction]
        #plt.title("Prediction: " + speech.title())
        #plt.show()
        text = str(speech.title())
        sp = gTTS(text=text, lang=language, slow=False)
        sp.save('/home/pi/tf/prediction.mp3')
        os.system('omxplayer /home/pi/tf/prediction.mp3')
        os.system('sudo rm /home/pi/cap.jpg')
        text = 'Ready'
        os.system('omxplayer /home/pi/tf/ready.mp3')
        print('Ready')
except:
    print('Something went wrong')
    text = 'Something went wrong'
    sp = gTTS(text=text, lang=language, slow=False)
    sp.save('/home/pi/tf/error.mp3')
    os.system('omxplayer /home/pi/tf/error.mp3')

