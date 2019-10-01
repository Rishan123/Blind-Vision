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
path = "/home/pi/Pictures/landmark.jpeg"
                        
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
