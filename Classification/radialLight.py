from math import sqrt
from PIL import Image

#to get center take object and divide hieght and width by two
center = [100, 200] #get from img
width = 100 #get from img pixels
height= 100 # get from img pix

#todo add image cleaner?: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_photo/py_non_local_means/py_non_local_means.html

#Get galaxy Light Profile

#convert to RGB image 
#TODO change image names and make it work for all imgs
img = Image.open("nibbler.jpg").convert('RGB')
img.save('NibblerRGB.png')

# define change in rad and first rad
deltaH = height / 40
deltaW = width /40
radh = round(center[0] + deltaH)
radw = round(center[1] + deltaW)
prevBrightness = 0

#split into 20 points to plot
for i in range (0,20):

  for x in range(-radw, radw):
    for y in range (-radh, radh):
      pixelRGB = img.getpixel((x, y))
      R,G,B = pixelRGB
      luminanceVal = (.2126*R + .7152*G + .0722*B) #get luminance value
      brightness += luminanceVal

  #plot point
  
  #radh = radh + deltah
  #radw += deltaw

  #TrueBrightness = brightness - radialBrightness
  #add trueBrightness to array 
  # i+1 and repeat

#Unsupervised learning algorithm
