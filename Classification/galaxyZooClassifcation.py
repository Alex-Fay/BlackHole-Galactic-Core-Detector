#Alex Fay CNN for Galaxy Classification
#Original Code from Tensorflow CNN Tutorial: changes to activation layers, channels, and more for optimization of specific class
#added layers for accuracy

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt

#=====importing data=======
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data() #change data
train_images, test_images = train_images / 255.0, test_images / 255.0

class_names = ['SpiralA', 'SpiralB', 'SpiralC', 'SpiralBa', 'SpiralSBb',
               'SpiralBc', 'Elliptical', 'Irregular', 'Star', 'Other']

#----------Plot-----------
plt.figure(figsize=(10,10))
for i in range(9):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i][0]])
plt.show()

#=========Convolutional Base=========
#relu = rectified linear unit
model = models.Sequential() #not from API
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3))) #32 channels, 3by3 kernel size
model.add(layers.MaxPooling2D((2, 2))) #2d Pooling Layer
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

#================Layer 1=============
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

#=========Layer 2========
model.add(layers.Flatten())
model.add(layers.Dense(32, activation='softmax'))
model.add(layers.Dense(10))

#=========Layer 3=========
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='linear'))
model.add(layers.Dense(10))


#====Layer 4========
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10))

#============Compile and Train Model==========
model.compile(optimizer='adam',
              loss= 'mean_squared_error',
              metrics=['accuracy'])

history = model.fit(train_images, train_labels, epochs=10, 
                    validation_data=(test_images, test_labels))

#Evaluate Model with Plot: Accuracy to Epoch
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0.5, 1])
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)

print(test_acc)
