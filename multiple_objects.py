import os
from google.cloud import vision
import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Downloads/blind-eye-3e6495bea978.json"
path = "/home/pi/Pictures/anger.jpeg"

def detect_object(path):    
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        if object_.score >= 0.5:
            print('\n{} '.format(object_.name))
            
detect_object(path)
            
