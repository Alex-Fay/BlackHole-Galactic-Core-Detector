#Alex Fay 4/3/2020
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#======== Variables ========= 
center = [60, 60]
img = cv.imread("Brightness13-16100.jpg")

#=========== Radial Light Profile Function =============
def radial_profile(img, center):
    a, b, c = np.indices(img.shape)
    r = np.sqrt((a - center[0])**2 + (b - center[1])**2)
    r = r.astype(np.int)
    tbin = np.bincount(r.ravel(), img.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile

#============ plot points ===============
import matplotlib
from matplotlib import pyplot as plt
Y = radial_profile(img, center)
plt.plot(Y, 'r')
plt.title("Image Luminosity vs. Radius")
plt.ylabel('Luminance pixel magnitude')
plt.xlabel('Radius in pixels')
plt.show()
