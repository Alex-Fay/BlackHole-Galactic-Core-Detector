#Alex Fay 4/29/2020
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

#Run file seperatly for each type of galaxy
#======== Variables ========= 
readFile = "Spiral_List.csv" #or other csv 
radialCSV = pd.DataFrame()
df = pd.read_csv(readFile)
imgName = df['ImgName']
labelCol = df['Label']
item = 0
print("ReadCSV")

#======== Find Rotation Theta =========
from PIL import Image
import math

def findOrigin(i):
  maxBrt, x, y, x0, y0 = 0, 0, 0, 0, 0 #origin will be brightest pixel value
  img = Image.open("./images_training/train/" + str(imgName[i]))
  for x in range(s):
    for y in range(s):
      brt = sum(img.getpixel((x, y)))
      if brt > maxBrt: 
        maxBrt = brt
        x0 = x; y0 = y #oriin values (x0, y0)
      y +=1
    x+=1
  print("x0", x0, "y0", y0)
  return x0, y0

#should combine, not sure how to break with two for loops/ out of time
def findXRadius(x0, y0, i):
  img = Image.open("./images_training/train/" + str(imgName[i]))
  a = 0
  for x in range(x0, s): #get minor axis
    brt = sum(img.getpixel((x, y0)))
    if(brt < 200): x+=1
    else: a = x
    return a

def findYRadius(x0, y0, i):
  img = Image.open("./images_training/train/" + str(imgName[i]))
  b = 0
  for y in range(y0, s): #major axis
    brt = sum(img.getpixel((x0, y)))
    if(brt < 200): #background space noise brightness
      b = y
      return b

def findTheta(x0, y0, a, b):
  top = math.sqrt(abs(y0**2 - b**2))
  bottom = math.sqrt(abs(x0**2 - a**2))
  if(bottom == 0): theta = 0
  else:
    theta = math.acos(-1 * top/bottom)
  return theta
print("Complete Rotation")

#=========== Radial Light Profile Function =============
def radial_profile(img, center):
    a, b, c = np.indices(img.shape) # a and b are (x, y) of pixel location
    r = np.sqrt((a - center[0])**2 + (b - center[1])**2) #get radius using distance eqn
    r = r.astype(np.int) 
    tbin = np.bincount(r.ravel(), img.ravel()) #integrate pixel brightness with increasing r
    nr = np.bincount(r.ravel()) #get dr over length r
    radialprofile = tbin / nr #divide integral of light profile by r change
    predictRadial = np.flipud(radialprofile) #reverse array 
    sumRad = np.sum(radialprofile)
    return radialprofile, predictRadial, sumRad
print("Complete Radial")

#====== MAIN =======
for item in df.index:
  img = cv.imread('./images_training/train/' + str(imgName[item])) #TODO: change to full csv file
  print(img.shape)
  s, t, v = img.shape
  center =[(s/2), (t/2)]
  print("center", center)
  Y, predictRadial, sumRad = radial_profile(img, center)
  if (sumRad > 1500): #ignore to distant galaxies
    x0, y0 = findOrigin(item)
    a = findXRadius(x0, y0, item)
    b = findYRadius(x0, y0, item)
    print(a, b)
    theta = findTheta(x0, y0, a, b)
    np.insert(predictRadial,0, theta)
    #add elements to csv
    radialCSV.loc[item] = mydataframe.append(list(predictRadial), index = item)
    item +=1
  else: item +=1
  
radialCSV.to_csv("Spiral_radial.csv")
#TODO Put each predict array into new column
#============ plot points ===============
import matplotlib
from matplotlib import pyplot as plt
plt.plot(Y, 'r')
plt.title("Image Luminosity vs. Radius")
plt.ylabel('Luminance pixel magnitude')
plt.xlabel('Radius from center')
plt.show()
