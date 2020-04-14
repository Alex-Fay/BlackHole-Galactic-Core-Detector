#Alex Fay 4/3-12/2020 Galaxy Sorter CNN
#Using 55,000 images for training, 6,100 for testing
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
from keras.models import Sequential, Model
from keras.layers.core import Flatten, Dense, Dropout, Lambda, Reshape
from keras.layers import Input
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Conv2D, MaxPooling2D, Activation
from keras.optimizers import SGD, RMSprop, Adam
import cv2 #open CV for cropping image
import matplotlib.image as mpimg
import os
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from keras import backend as K
import pdb #debugger

#==========unzip training data=======
import zipfile
zip_ref = zipfile.ZipFile("images_training.zip", "r")
zip_ref.extractall() #data is too big for google drive and github even in zip :/
zip_ref.close()

import zipfile
zip_ref = zipfile.ZipFile("Testing_Images.zip", "r")
zip_ref.extractall()
zip_ref.close()

#Read CSV For Cropping Images
file = "FinalResults.csv"
df = pd.read_csv(file)
galaxyID = df['GalaxyID']
Label = df['Label']

#Testing Data Read
testData = 'trainLabels.csv'

import pandas as pd
import cv2

#===========Cropping Images==============
#SDSS Galaxy Set is 120 by 120 pixels, cropping to get similar data & delete empty space
def cropImages():
  for i in df.index & range(0, 61000):
    try:
      imgName = "./images_training/" + str(galaxyID[i]) + ".jpg"
      img = cv2.imread(imgName)
      img = img[106:106*3, 106:106*3]
      #plt.figure();plt.imshow(crop_img);plt.show()
      cv2.waitKey(0)
      cv2.imwrite(imgName, img)
      print("Success")
    except:
      print("Image Missing from DataBase")
  return img

cropImages()

#=============training data init===========
train_file_path = 'FinalResults.csv'
test_file_path = 'trainLabels.csv'

#Cuts out all in csv except galaxy name, returns list w/ commas
ary = np.genfromtxt(train_file_path, delimiter= ',' , dtype = str)
train_labels = list(ary[:,-1])
tempAry = np.genfromtxt(test_file_path, dtype = str, delimiter= ",")
test_labels = list(tempAry[:, -1])
train_images = "./images_training/"
test_images = "./Testing_Images/"

#=======CNN========
def ConvBlock(layers, model, filters):
    for i in range(layers): 
        model.add(ZeroPadding2D((2,2)))  # zero padding of size 1
        model.add(Convolution2D(filters, 3, 3, activation='relu'))  # 3x3 filter size 
    model.add(MaxPooling2D((2,2), strides=(2,2)))

def FCBlock(model):
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    
def VGG_16():
    model = Sequential()
    model.add(Lambda(lambda x : x, input_shape=(3,106,106)))
    
    ConvBlock(2, model, 64)
    ConvBlock(2, model, 128)
    ConvBlock(3, model, 256)
    ConvBlock(3, model, 512)
    ConvBlock(3, model, 512)

    model.add(Flatten())
    FCBlock(model)
    FCBlock(model)
    
    model.add(Dense(37, activation = 'sigmoid'))
    return model

#======MAIN========
#cropImages()
# Compile 
optimizer = RMSprop(lr=1e-6)
model = VGG_16()
model.compile(loss='mean_squared_error', optimizer=optimizer)

temp_data = (test_images, test_labels)
print(test_labels)

fitCNN = model.fit(train_images, train_labels, epochs= 40, 
                    validation_data = temp_data)
model.summary()

#========Plot======
plt.plot(fitCNN.fitCNN['accuracy'], label = 'accuracy')
plt.plot(fitCNN.fitCNN['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc= 'upper right')

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose = 2)
print(test_acc)
