# -*- coding: utf-8 -*-
"""Car_Dog_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16jzOE2KhyaR8skoa16cPkZ6gvgmaCqo9
"""

!mkdir -p ~/.kaggle
!cp kaggle.json  ~/.kaggle/

!kaggle datasets download -d salader/dogs-vs-cats

import zipfile
zip_file=zipfile.ZipFile('/content/dogs-vs-cats.zip','r')
zip_file.extractall('/content')
zip_file.close()

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout

from keras.utils.image_dataset import image_dataset_from_directory
# Generators
train_generator=image_dataset_from_directory(
    directory='/content/train',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)
test_generator=image_dataset_from_directory(
    directory='/content/test',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(256,256)
)

# Normalize
def process(image,label):
  image=tf.cast(image/255,tf.float32)
  return image,label
train_generator=train_generator.map(process)
test_generator=test_generator.map(process)

# Create CNN Model

model=Sequential()
model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2),strides=2,padding='valid'))

model.add(Flatten())
model.add(Dense(128,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
model.fit(train_generator,epochs=10,validation_data=test_generator)

import cv2
cat=cv2.imread('cat.png')
test_cat=cv2.resize(cat,(256,256))
test_input=test_cat.reshape((1,256,256,3))
model.predict(test_input)