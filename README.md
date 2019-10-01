# Blind-Vision #

This repository is all about the creation of Blind Vision. Blind Vision will be an assistant for blind people that uses a Raspberry Pi to tell what is in front of the wearer.

### Table of Contents:  

* Installing Google Cloud Vision
* Installing Google Text-To-Speech (gTTS)
* Connecting the hardware
* Testing the hardware
* The main program

And of course, all of this is either done In the Terminal, or Python 3.

### Installing Google Cloud Vision (GCV) ###

First of all, create a new project with the name Blind-Vision (or any name you prefer). Then create a service account key by clicking Credentials and then download it. Then, in the Terminal, do:

```
pip install --upgrade google-cloud-vision
```
For downloading the library for Python 2.
And then do:

```
pip3 install --upgrade google-cloud-vision
```
Then create a test program called ```test_vision.py``` and enter the following:

```
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('resources/wakeupcat.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
    
```
