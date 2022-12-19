import numpy as np
import time
from PIL import Image
from tensorflow.lite.python import interpreter as interpreter_wrapper
from gpiozero import Button
from time import sleep
from picamera import PiCamera
# from gtts import gTTS
import os
import subprocess

button = Button(15, pull_up=False)

print("loaded variables and functions")
def espeak(text: str, pitch: int=50) -> int:
    # Use espeak to convert text to speech
    return subprocess.run(['espeak', '-ven+f3', '-k5', '-s150', text]).returncode

def load_labels(filename):
    my_labels = []
    input_file = open(filename, 'r')
    for l in input_file:
        my_labels.append(l.strip())
    return my_labels
print("loaded functions. Starting main program")

while True:
    camera = PiCamera()
    floating_model = False
    predictions = []
    print("Ready")
    espeak("Ready")
    print("Waiting for button press")
#     camera.start_preview()
    button.wait_for_press()
#     camera.stop_preview()
    camera.capture('/home/pi/Blind-Vision/cap.jpg')
    image = '/home/pi/Blind-Vision/cap.jpg'
    camera.close()
#     image = "/home/pi/Blind-Vision/v2/Object_recognition/street.jpeg"
    model_file = "/home/pi/Blind-Vision/v2/Object_recognition/inception_v4_299_quant.tflite"
    label_file = "/home/pi/Blind-Vision/v2/Object_recognition/labels.txt"
    input_mean = 127.5
    input_std = 127.5
    num_threads = 1

    interpreter = interpreter_wrapper.Interpreter(model_path=model_file)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
  # check the type of the input tensor
    if input_details[0]['dtype'] == np.float32:
        floating_model = True
  # NxHxWxC, H:1, W:2
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    img = Image.open(image)
    img = img.resize((width, height))
    # add N dim
    input_data = np.expand_dims(img, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_num_threads(int(num_threads))
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)
    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    for i in top_k:
        confidence = float(results[i])
        if floating_model:
            print('{0:08.6f}'.format(confidence)+":", labels[i])
            if confidence >= 0.5:
                print(predictions[0])# The first (and only) item in the list. This will be spoken in the real project
                espeak('This is a ' + str(predictions[0]))
            else:
                espeak("Unidentified object")
        else:
            print((confidence/255.0),":", labels[i])
            if (confidence/255.0) >= 0.5:
                predictions.append(labels[i]) # This will be the object with the highest confidence, since the recognition algorithm lists the possibilities in order of their confidence
                espeak('This is a ' + str(labels[i]))
            else:
                espeak("I do not know what this object is")
            break
    
#         if (confidence/255.0) >= 0.5:
#             print(predictions[0])# The first (and only) item in the list. This will be spoken in the real project
#             espeak(str(predictions[0]))
#         else:
#             espeak("Unidentified object")

