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
from keras.preprocessing.image import ImageDataGenerator

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
from os import listdir
import random
from numpy import asarray
from numpy import save
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from shutil import copyfile #for creating training data

train_file_path = 'HubbleImageLabels.csv'
test_file_path = 'trainLabels.csv'
src_directory = "./images_training/"
folder = "./images_training/"

#======Create Data for training and testing=========
subdirs = ['train/', 'test/'] #prexisting folders in images_training (manual)
for subdir in subdirs:  #Create subfolders for training and test
  labeldirs = ['STAR', 'Elliptical', 'Elliptical_Cigar', 'Spiral', 'Bar_Spiral', 'Lenticular','Irregular']
  for labl in labeldirs:
    newdir = folder + subdir + labl #make folder for each type of img
    os.makedirs(newdir, exist_ok = True)

#save 25 percent of data for testing
random.seed(1) #random num generator
val_ratio = .25
src_directory = './images_training/train/'

#split data into testing and training folders by class
for file in listdir(src_directory):
  src = src_directory + file
  dst_dir = './images_training/train/'
  imgType = file.split(".")
  if (random.random() < val_ratio):
    dst_dir = './images_training/test/'
  dst = dst_dir + imgType[0] + "/" + file 
  try:
    copyfile(src, dst) #i.e. move elliptical to train/elliptical/
  except:
    print("Missing:" + file)

#=======CNN==================
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
    model.add(Lambda(lambda x : x, input_shape=(210,210,3)))
    
    ConvBlock(2, model, 64)
    ConvBlock(2, model, 128)
    ConvBlock(3, model, 256)
    ConvBlock(3, model, 512)
    ConvBlock(3, model, 512)

    model.add(Flatten())
    FCBlock(model)
    FCBlock(model)
    
    model.add(Dense(9, activation = 'sigmoid'))
    return model

#======MAIN========
#datagen required for keras
datagen = ImageDataGenerator(rescale =1.0/255.0)
#cropImages()

train_it = datagen.flow_from_directory('./images_training/train/', class_mode = "categorical", batch_size = 64, target_size = (210, 210))
test_it = datagen.flow_from_directory('./images_training/test/', class_mode = "categorical", batch_size = 64, target_size = (210, 210))

# Compile 
optimizer = RMSprop(lr=1e-6)
model = VGG_16()
model.compile(loss='mean_squared_error', optimizer=optimizer)

fitCNN = model.fit_generator(train_it, steps_per_epoch = len(train_it),epochs= 40, 
                    validation_data = test_it, validation_steps = len(test_it))
model.summary()

#========Plot======
plt.plot(fitCNN.fitCNN['accuracy'], label = 'accuracy')
plt.plot(fitCNN.fitCNN['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc= 'upper right')

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose = 2)
print(test_acc)
