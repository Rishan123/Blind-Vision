import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
import numpy as np
import PIL.Image as Image
import matplotlib.pylab as plt

tf.enable_eager_execution()

shape = (224, 224)

epochs = 1
labels = '/home/pi/tf/labels.txt'
labels = np.array(open(labels).read().splitlines())

img = '/home/pi/tf/cat.jpeg'
img = Image.open(img).resize(shape)
img = np.array(img)/255.0
img = np.reshape(img, (224, 224, 3))

train = tfds.load(name="caltech101", split=tfds.Split.TRAIN)

assert isinstance(train, tf.data.Dataset)

example, = train.take(1)
image, label = example["image"], example["label"]

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(224,224,3)),
    keras.layers.Dense(128, activation='relu'), 
    keras.layers.Dense(101, activation='softmax') 
])

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(image, label, epochs=epochs,  verbose=2) 
         # validation_data=(test_images, test_labels))
          ##)

result = model.predict(img[np.newaxis, ...])
predicted_class = np.argmax(result[0], axis=-1)
prediction = labels[predicted_class]
print(prediction)
plt.imshow(img)
plt.axis('off')
plt.title("Prediction: " + prediction.title())
plt.show()
