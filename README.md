# Blind-Vision #

This repository is all about the creation of Blind Vision. Blind Vision will be an assistant for blind people that uses a Raspberry Pi to tell what is in front of the wearer.

## Table of Contents:  

* Installing Google Cloud Vision
* Installing Google Text-To-Speech (gTTS)
* The main program

And of course, all of this is either done In the Terminal, or Python 3.

## Installing Google Cloud Vision (GCV) ##

First of all, create a new project with the name Blind-Vision (or any name you prefer). Then fill in your billing details. If purchasing Google Cloud Vision isn't possible, don't worry, we will be using OpenCV for the finished product. Then create a service account key by clicking Credentials and then download it. In the Terminal, do:

### Python 2 ###
```
pip install --upgrade google-cloud-vision
```

### Python 3 ###
```
pip3 install --upgrade google-cloud-vision
```
For downloading for Python 3.

Then create a test program called ```test_vision.py``` and enter the following:
Don't forget to replace ```/YOUR/SERVICE/ACCOUNT/CREDENTIALS/ABCDEF.JSON``` with the path to the credentials and the name.
```
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/YOUR/SERVICE/ACCOUNT/CREDENTIALS/ABCDEF.JSON"

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)
        break
        
detect_labels("/home/pi/Pictures/happy.jpeg")

    
```


## Installing Google Text-To-Speech ##

Installing gTTS is free of cost and is really easy to install. Just use the single command on the Terminal:

### Python 2 ###
```
pip install gTTS
```

### Python 3 ###

```
pip3 install gTTS
```

## The main program ##

So, assuming you have all the hardware connected (if not, follow this [link](https://github.com/Rishan123/Blind-Vision/tree/master/Hardware)), let's get to the main program!
Don't forget to replace ```/YOUR/SERVICE/ACCOUNT/CREDENTIALS/ABCDEF.JSON``` with the path to the credentials and the name.

```

import os
from google.cloud import vision
import io
from gtts import gTTS
from time import sleep
import RPi.GPIO as GPIO

button = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.IN)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Downloads/blind-eye-3e6495bea978.json"
path = "home/pi/blind-vision/Pictures/landmark.jpeg"
                        
def face(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'is VERY UNLIKELY', 'is UNLIKELY', 'is POSSIBLE',
                       'is LIKELY', ' is VERY LIKELY')
    for face in faces:
        if face.anger_likelihood > face.joy_likelihood and face.anger_likelihood > face.surprise_likelihood: 
            print('anger {}'.format(likelihood_name[face.anger_likelihood]))
            speech = 'anger: {}'.format(likelihood_name[face.anger_likelihood])
            tts = gTTS(text=speech, lang="en")
            tts.save("/home/pi/Music/speech.mp3")
        
        elif face.joy_likelihood > face.anger_likelihood and face.joy_likelihood > face.surprise_likelihood: 
            print('joy {}'.format(likelihood_name[face.joy_likelihood]))
            speech = 'joy: {}'.format(likelihood_name[face.joy_likelihood])
            tts = gTTS(text=speech, lang="en")
            tts.save("/home/pi/Music/speech.mp3")
        
        else:
            if face.surprise_likelihood > face.joy_likelihood and face.surprise_likelihood > face.anger_likelihood: 
                print('surprise {}'.format(likelihood_name[face.surprise_likelihood]))
                speech = 'surprise: {}'.format(likelihood_name[face.surprise_likelihood])
                tts = gTTS(text=speech, lang="en")
                tts.save("/home/pi/Music/speech.mp3")
        os.system("omxplayer /home/pi/Music/speech.mp3")
        
        break
        
        
def text(path):
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))
        speech = str(text.description)
        tts = gTTS(text=speech, lang="en")
        tts.save("/home/pi/Music/speech.mp3")
        os.system("omxplayer /home/pi/Music/speech.mp3")
        break
        

                        
                        
def landmark(path):
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    for landmark in landmarks:
        print(landmark.description)
        speech = str(landmark.description)
        tts = gTTS(text=speech, lang="en")
        tts.save("/home/pi/Music/speech.mp3")
        os.system("omxplayer /home/pi/Music/speech.mp3")
        break
        
def main(path):

    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
        
    for object_ in objects:
        if object_.score >= 0.1:
            if object_.name == "Top":
                break
            ## Add in the landmarks() function
            if object_.name == "Building":
                landmark(path)
            else:
                print('\n{} (confidence: {})'.format(object_.name, object_.score))
                
    for label in labels:
        if label.description == "Text":
            print("Text Detected")
            text(path)
            break
        if label.description == "Hair" or "Woman":
            face(path)
            break

                    
        
            
while True:
    if GPIO.input(button):
        print("ON")
        main(path)

```
