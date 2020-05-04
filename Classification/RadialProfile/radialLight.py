#Alex Fay 4/29/2020
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

#Run file seperatly for each type of galaxy
#======== Variables ========= 
readFile = "Bar_Spiral_List.csv" #or other csv 
col, picNames, rotation = [], [], []
for j in range(0, 300): col.append(str(j))
radialCSV = pd.DataFrame()
df = pd.read_csv(readFile)
imgName = df['ImgName']
labelCol = df['Label']
item = 0
print("ReadCSV")

#======== Find Rotation Theta =========
from PIL import Image
import math

def findOrigin(item, s):
  maxBrt, x, y, x0, y0 = 0, 0, 0, 0, 0 #origin will be brightest pixel value
  img = Image.open('./images_training/train/' + str(imgName[i])) 
  for x in range(s):
    for y in range(s):
      brt = sum(img.getpixel((x,y)))
      if brt > maxBrt: 
        maxBrt = brt
        x0 = x; y0 = y #oriin values (x0, y0)
      y +=1
    x+=1
  print("x0", x0, "y0", y0)
  return x0, y0

#should combine, not sure how to break with two for loops/ out of time
def findXRadius(x0, y0, i, s):
  img = Image.open('./images_training/train/' + str(imgName[i]))
  a = 0
  for x in range(x0, s): #get minor axis
    if a == 0:
      brt = sum(img.getpixel((x, y0)))
      if(brt > 200): x+=1
      else: 
        a = x
  return a

def findYRadius(x0, y0, i, s):
  img = Image.open('./images_training/train/' + str(imgName[i]))
  b = 0
  for y in range(y0, s): #get minor axis
    if b == 0:
      brt = sum(img.getpixel((x0, y)))
      if(brt > 200): y+=1
      else: 
        b = y
  return b

def findTheta(x0, y0, a, b):
  top = math.sqrt(abs(y0**2 - b**2))
  bottom = math.sqrt(abs(x0**2 - a**2))
  print("Top", top, "Bottom", bottom)
  if(bottom == 0): theta = 0
  else:
    temp = top/bottom
    temp = float(str(temp-int(temp))[1:])
    print("temp", temp)
    theta = math.acos(-1 * (temp))
    print(theta)
  return theta

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
  s, t, v = img.shape
  center =[(s/2), (t/2)]
  Y, predictRadial, sumRad = radial_profile(img, center)
  if (sumRad > 1500): #ignore to distant galaxies
    x0, y0 = findOrigin(item, s)
    a = findXRadius(x0, y0, item, s)
    b = findYRadius(x0, y0, item, s)
    theta = findTheta(x0, y0, a, b)
    rotation.append(theta)
    picNames.append(imgName[item])
    print("a", a, "b", b, "s", s, "x0", x0, y0, theta)
    #add elements to csv
    temp = pd.DataFrame(predictRadial.reshape(-1, len(predictRadial)))
    radialCSV = radialCSV.append(temp)
    item +=1
  else: item +=1

radialCSV["ImgName"] = picNames
radialCSV["theta"] = rotation
radialCSV.to_csv("Spiral_radial.csv")

#TODO Put each predict array into new column
#np.insert(predictRadial,0, theta)
#create name array and theta array
#============ plot points ===============
import matplotlib
from matplotlib import pyplot as plt
plt.plot(Y, 'r')
plt.title("Image Luminosity vs. Radius")
plt.ylabel('Luminance pixel magnitude')
plt.xlabel('Radius from center')
plt.show()
