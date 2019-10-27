# Blind-Vision #

This repository is all about the creation of Blind Vision. Blind Vision will be an assistant for blind people that uses a Raspberry Pi to tell what is in front of the wearer.

## Table of Contents:  

* Installing Tensorflow                                  
* Installing Google Text-To-Speech (gTTS)
* Getting started with Tensorflow
* Installing Tensorflow Hub

## Installing Tensorflow ##

Tensorflow is a machine learning framework which Google has provided. We will be using this in our project for the image classification. To install Tensorflow for Python 3:

[Link to Tensorflow's website](http://tensorflow.org)

```
sudo pip3 install tensorflow 
```
This installation will take a long time, so you might take a stroll in the park or have a cup of tea for a few minutes.


## Installing Google Text-To-Speech ##

Installing gTTS is free of cost and is really easy to install. Just use the single command on the Terminal:

### Python 2 ###
```
pip install gTTS
```

### Python 3 ###

```
pip3 install gTTS
```

## Getting started with Tensorflow ##

To test the installation of Tensorflow, go into the Terminal and run:
```                                                   
python3
```
then run:
```
import tensorflow as tf
```

### NOTE: There will be a long set of warnings, especially if your Python package is higher than 3.5 . This is because Tensorflow is designed to work with Python3.5, but nothing to worry. ###

## Installing Tensorflow Hub ##

Tensorflow Hub is a free-of-charge collection of datasets which can be downloaded from a simple Python program.
```
pip3 install --upgrade tensorflow-hub
```
To test the installation, go to the Terminal, (CTRL,ALT,T) and type in ```python3```. You will then be in the Python environment from the Terminal. Then run:
```
import tensorflow_hub as hub
```
You should be back at the Python prompt. To exit, type in ```exit()``` or CTRL-D.
Done!
