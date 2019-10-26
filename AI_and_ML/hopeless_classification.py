import tensorflow as tf
import numpy as np
import PIL.Image as Image
from tensorflow import keras

tf.compat.v1.enable_eager_execution()

img = '/home/pi/tf/lobster.jpeg'

ds = keras.datasets.cifar100

(train_images, train_labels), (test_images, test_labels) = ds.load_data()
num,arg1,arg2,arg3 = train_images.shape

shape = (arg1, arg2)
img = Image.open(img).resize(shape)
img = np.array(img)/255.0

img = np.reshape(img, (arg1, arg2, arg3))
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(arg1, arg2, arg3)),#224,224,3
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(100, activation='softmax')
])


model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
    )

model.fit(train_images, train_labels, epochs=10)

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print('\nTest accuracy:', test_acc)
print('\nTest loss:', test_loss)

result = model.predict(img[np.newaxis, ...])
