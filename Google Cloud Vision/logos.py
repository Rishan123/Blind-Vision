import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Downloads/blind-eye-3e6495bea978.json"
def detect_logos(path):
    """Detects logos in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)
detect_logos("/home/pi/Pictures/logo.png")