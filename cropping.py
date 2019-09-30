import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/Downloads/blind-eye-3e6495bea978.json"
def detect_crop_hints(path):
    """Detects crop hints in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    crop_hints_params = vision.types.CropHintsParams(aspect_ratios=[1.77])
    image_context = vision.types.ImageContext(
        crop_hints_params=crop_hints_params)

    response = client.crop_hints(image=image, image_context=image_context)
    hints = response.crop_hints_annotation.crop_hints

    for n, hint in enumerate(hints):
        print('\nCrop Hint: {}'.format(n))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in hint.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        
detect_crop_hints("/home/pi/Pictures/faces.jpeg")