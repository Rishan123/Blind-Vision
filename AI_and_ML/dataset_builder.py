import tensorflow as tf
import tensorflow_datasets as tfds

def download_ds(name,split):
    # Loads the dataset
    ds_builder = tfds.builder(name)
    ds_builder.download_and_prepare()
    ds_train = ds_builder.as_dataset(split=split)
    return ds_train



