#Alex Fay 4/3/2020
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

#Run file seperatly for each type of galaxy
#======== Variables ========= 
center = [60, 60]
readFile = "HubbleImageLabels.csv" #or other csv 
df = pd.read_csv(readFile)
imageCSV = df['ImgName']
labelCol = df['Label']
item = 0

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

#====== Profile to CSV =======
for item in df.index & range(1, 1):
  noise = 5 #avg background space
  img = cv.imread(imageCSV[i]) #TODO: change to full csv file
  Y, predictRadial, sumRad = radial_profile(img, center)
  if (sumRad > 1500): #ignore to distant galaxies
    ndf = pd.DataFrame(list(zip(predictRadial)))
    ndf.to_csv("example.csv")
    item +=1
  else: item +=1

#============ plot points ===============
import matplotlib
from matplotlib import pyplot as plt
plt.plot(Y, 'r')
plt.title("Image Luminosity vs. Radius")
plt.ylabel('Luminance pixel magnitude')
plt.xlabel('Radius from center')
plt.show()
