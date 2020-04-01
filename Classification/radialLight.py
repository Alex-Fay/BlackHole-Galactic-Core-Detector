#@Alex Fay 3/30-1/2020
from math import sqrt
from PIL import Image
import numpy as np

#to get center take object and divide hieght and width by two
center = [800, 400] #get from img
width = 1600 #get from img pixels
height= 800 # get from img pix
brightness = 0

#todo add image cleaner?: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_photo/py_non_local_means/py_non_local_means.html

#============= Get galaxy Light Profile =====================

#convert to RGB image 
#TODO change image names and make it work for all imgs
img = Image.open("galaxy.png").convert('RGB')
img.save('GalRGB.png')

# define change in rad and first rad
deltaH = height / 40
deltaW = width /40
radh = int(center[0] + deltaH)
negRadh = int(center[0] - deltaH)
radw = int(center[1] + deltaW)
negRadw = int(center[1] - deltaW)
prevBrightness, trueBrightness, area = 0, 0, 0
luminousPlot = np.array(brightness)
areaPlot = np.array(area)

#split into 20 points to plot
for i in range(0,20):

  #go through each pixel and add brightness 
  for x in range(0, 485): #negRadw, radw                   #<=======TODO
    for y in range(0, 624): #negRadh, radh
      pixelRGB = img.getpixel((x, y))
      R,G,B = pixelRGB
      luminanceVal = (.2126*R + .7152*G + .0722*B) #get luminance value
      brightness += luminanceVal

  trueBrightness = round(brightness - prevBrightness) # outercircle - inner circle
  area = radh * radw

  #update values for plotting and next circle
  luminousPlot = np.append(luminousPlot, trueBrightness)
  areaPlot = np.append(areaPlot, area)
  radh += deltaH
  negRadh -= deltaH
  radw += deltaW
  negRadw -= deltaW
  i += 1

print("BrightNess:", luminousPlot)
print("Area", areaPlot)

#plot point
import matplotlib
from matplotlib import pyplot as plt
plt.plot(areaPlot, luminousPlot, 'r')
plt.title("Brightness to Area")
plt.ylabel('Brightness in luminance pixel magnitude')
plt.xlabel('Area in pixels')
plt.show()

#Unsupervised learning algorithm
