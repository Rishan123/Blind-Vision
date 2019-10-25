import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import numpy as np

tf.compat.v1.enable_eager_execution()
train_labels,train_images = tfds.load(name="cifar100", split="train",as_supervised=True)
cifar_test, info = tfds.load(name="cifar100", split="test",with_info=True)
# fig = tfds.show_examples(info, cifar_train)


