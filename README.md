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

