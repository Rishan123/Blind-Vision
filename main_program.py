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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Downloads/blind-eye-3e6495bea978.json"
path = "/home/pi/blind-vision/capture.jpeg"
trig = 4
echo = 17
print("Press button to start")
def get_pulse_time_v2(trig_pin, echo_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    cnt1 = 0
    cnt2 = 0

    GPIO.output(trig_pin, True)
    sleep(0.00001)
    GPIO.output(trig_pin, False)

    start = time()
    while GPIO.input(echo_pin) == 0:
        start = time()
        cnt1 += 1
        if cnt1 > 1000:
            break

    stop = time()
    while GPIO.input(echo_pin) == 1:
        stop = time()
        cnt2 += 1
        if cnt2 > 1000:
            break

    return (stop - start)

def calculate_distance(duration):
    speed = 343
    distance = speed * duration / 2
    return distance
    
    
def calc_dist_cm_v2(trig_pin, echo_pin):
    duration = get_pulse_time_v2(trig_pin, echo_pin)
    distance = calculate_distance(duration)
    distance_cm = int(distance*10000)
    return distance_cm

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
        
    for object_ in objects:
        if object_.name == "Person":
            speech = "Face Detected"
            tts = gTTS(text=speech, lang="en")
            tts.save("/home/pi/Music/speech.mp3")
            os.system("omxplayer /home/pi/Music/speech.mp3")
        if object_.score >= 0.6:
            if object_.name == "Top":
                break
            elif object_.name == "Building":
                landmark(path)
            else:
                print('\n{} '.format(object_.name))
                
                speech = (object_.name)
                tts = gTTS(text=speech, lang="en")
                tts.save("/home/pi/Music/speech.mp3")
                os.system("omxplayer /home/pi/Music/speech.mp3")
                
    for label in labels:
        if label.description == "Text":
            print("Text Detected")
            text(path)
            break
        if label.description == "Hair" or "Woman" or "Glasses" or "Person":
            print("Person Detected")
            speech = "Person Detected!"
            tts = gTTS(text=speech, lang="en")
            tts.save("/home/pi/Music/speech.mp3")
            os.system("omxplayer /home/pi/Music/speech.mp3")
            break

                    
        
            
while True:
    if GPIO.input(button):
        print("ON")
        main(path)
