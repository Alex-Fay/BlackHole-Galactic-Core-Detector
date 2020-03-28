!pip3 install pyyolo
!git clone --recursive https://github.com/astroCV/astroCV.git
!wget https://pjreddie.com/media/files/darknet19_448.conv.23
!git clone https://github.com/pjreddie/darknet.git
!git clone --recursive git@github.com:rayhou0710/pyyolo.git #import pyyolo

import pyyolo
import numpy as np
import sys
from PIL import Image, ImageEnhance
import matplotlib.patches as patches
import matplotlib.pyplot as plt 
import time

darknet_path = 'astroCV/galaxy_detection/data/darknet' #darknet path
datacfg = '../sdss.data' #relative to darknet path
cfgfile = '../sdss.cfg' #relative to darknet path
weightfile = '/mnt/data/astrocv/galaxy_sdss_hic.weights' # lupton rgb +2 brightness +2 contrast with ImageEnhance
thresh = 0.2  #detection probability threshold
hier_thresh = 0.5

#for each image data process
import glob
from PIL import Image
images = glob.glob("*.jpg")
for image in images:
  filename = Image.open(image) #filename = 'data/hic/1140_301_1_206.jpg' 

t1=time.time()
pyyolo.init(darknet_path, datacfg, cfgfile, weightfile) #init and load network
print('Initialization time = %5.3f seconds'%(time.time()-t1))
t1=time.time() #actually loading the image take most of the time
outputs = pyyolo.test(filename, thresh, hier_thresh, 0) #load image and process
print('Load from file + Image processing time = %5.3f seconds'%(time.time()-t1))
for output in outputs:
        print(output)    
pyyolo.cleanup()

!./darknet detector train cfg/sdss.data cfg/yolo.cfg darknet19_448.conv.23 -gpus 0,1
