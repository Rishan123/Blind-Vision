import os
from google.cloud import vision
import io
from gtts import gTTS
from time import sleep
import RPi.GPIO as GPIO
from picamera import PiCamera

button = 15
cam = PiCamera()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.IN)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Downloads/blind-vision-83a001e9c5f5.json"
path = "/home/pi/blind-vision/capture.jpeg"
trig = 4
echo = 17
print("Press button to start")

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

    cam.capture(path)
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations
    
    response = client.label_detection(image=image)
    labels = response.label_annotations
    face_count = 0
    for object_ in objects:
        if object_.name == "Glasses":
            face_count += 1
            break
        if object_.name == "Person" and face_count == 0:
            speech = "Face Detected"
            tts = gTTS(text=speech, lang="en")
            tts.save("/home/pi/Music/speech.mp3")
            os.system("omxplayer /home/pi/Music/speech.mp3")
            face_count += 1
        if object_.score >= 0.6:
            if object_.name == "Top":
                break
            elif object_.name == "Building":
                landmark(path)
            else:
                print('\n{}, {} '.format(object_.name,object_.score))
                speech = (object_.name)
                tts = gTTS(text=speech, lang="en")
                tts.save("/home/pi/Music/speech.mp3")
                os.system("omxplayer /home/pi/Music/speech.mp3")
                
    for label in labels:
        if label.description == "Text":
            print("Text Detected")
            text(path)
            break
        else:
            print(label.description)
            speech = label.description
            tts = gTTS(text=speech, lang="en")
            tts.save("/home/pi/Music/speech.mp3")
            os.system("omxplayer /home/pi/Music/speech.mp3")
            break       
            
while True:
    if GPIO.input(button):
        print("ON")
        main(path)
        