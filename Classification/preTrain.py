#Setup with need to importfiles for Google CoLab:
!sudo apt-get -y install gcc gfortran python-dev libopenblas-dev liblapack-dev cython
!sudo apt install python-pip*
!sudo pip install --upgrade pip*
!python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose 
!sudo pip install pytest*
!sudo apt-get install libxml2-dev libxslt-dev 
!sudo pip install h5py beautifulsoup4 pyyaml lxml pytz scikit-image objgraph setuptools mock bintrees*
!sudo pip install astropy --no-deps
!sudo pip install astroquery
!sudo apt-get install cmake git libgtk2.0-dev pkg-config libavformat-dev libswscale-dev
!sudo apt-get install curl m4 ruby texinfo libbz2-dev libcurl4-openssl-dev libexpat-dev libncurses-dev zlib1g-dev
!sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev
!sudo apt-get install libatlas-base-dev
!sudo apt-get install --assume-yes unzip ffmpeg qtbase5-dev
!sudo apt-get install --assume-yes libopencv-dev libgtk-3-dev libdc1394-22 libdc1394-22-dev libjpeg-dev
!sudo apt-get install --assume-yes libxine2-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
!sudo apt-get install --assume-yes libv4l-dev libtbb-dev libfaac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev
!sudo apt-get install --assume-yes libvorbis-dev libxvidcore-dev v4l-utils vtk6
!sudo apt-get install --assume-yes liblapacke-dev libgdal-dev checkinstall
!sudo apt-get install build-essential
!sudo apt-get update && sudo apt-get upgrade
!sudo apt-get purge nvidia* 
!sudo add-apt-repository ppa:graphics-drivers
!sudo apt-get update 
!sudo apt-get install nvidia-384 ##Replace 384 for the version you want. 384 was the latest version up to January 2018.
!echo -e "blacklist nouveau\nblacklist lbm-nouveau\noptions nouveau modeset=0\nalias nouveau off\nalias lbm-nouveau off\n" | sudo tee /etc/modprobe.d/blacklist-nouveau.conf
!echo options nouveau modeset=0 | sudo tee -a /etc/modprobe.d/nouveau-kms.conf
!sudo update-initramfs -u
!sudo dpkg -i cuda-repo-ubuntu1604-8-0-local_8.0.44-1_amd64.deb
!sudo apt-get update
!sudo apt-get install cuda
!sudo dpkg -i libcudnn5_5.1.10-1+cuda8.0_amd64.deb 
!sudo dpkg -i libcudnn5-dev_5.1.10-1+cuda8.0_amd64.deb 
!sudo dpkg -i libcudnn5-doc_5.1.10-1+cuda8.0_amd64.deb 
!git clone --recursive https://github.com/astroCV/opencv
!mkdir build
!cd build
!cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D FORCE_VTK=ON -D WITH_TBB=ON -D WITH_V4L=ON -D WITH_QT=ON -D WITH_OPENGL=ON -D WITH_CUBLAS=ON -D CUDA_NVCC_FLAGS="-D_FORCE_INLINES" -D WITH_GDAL=ON -D WITH_XINE=ON -D BUILD_EXAMPLES=ON ..
!make -j8
!wget https://pjreddie.com/media/files/darknet19_448.conv.23.
!./darknet detector train cfg/sdss.data cfg/yolo.cfg darknet19_448.conv.23 -gpus 0,1
#end need to have libs for AstroCV

#Begin training test on small iput data
import pyyolo
import numpy as np
import sys
from PIL import Image, ImageEnhance
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import time
import os.path

if sys.version_info[0] >= 3:
        from urllib.request import urlretrieve
else:
        # Not Python 3 - today, it is most likely to be Python 2
        # But note that this might need an update when Python 4
        # might be around one day
        from urllib import urlretrieve

##code from https://stackoverflow.com/questions/17960942/attributeerror-module-object-has-no-attribute-urlretrieve

darknet_path = './data/darknet' #darknet path
datacfg = '../sdss.data' #relative to darknet path
cfgfile = '../sdss.cfg' #relative to darknet path
weightfile = '/mnt/data/astrocv/galaxy_sdss_hic.weights'
filename = 'writable/downloaded.jpg' #relative to galaxy_detection path
url = "https://cdn.spacetelescope.org/archives/images/large/heic0916a.jpg"
if not os.path.isfile(filename):
    urllib.urlretrieve(url,filename)
thresh = 0.1  #detection threshold try 0.02 & 0.1
hier_thresh = 0.5

t1=time.time()
pyyolo.init(darknet_path, datacfg, cfgfile, weightfile) #init and load network
print('Initialization time = %5.3f seconds'%(time.time()-t1))
t1=time.time()
outputs = pyyolo.test(filename, thresh, hier_thresh, 0) #load image and process
print('Image processing time = %5.3f seconds'%(time.time()-t1))
for output in outputs:
        print(output)
pyyolo.cleanup()

#plot image and detections
img = Image.open(filename)
contrast = ImageEnhance.Contrast(img)
img2 = contrast.enhance(1)
fig,ax = plt.subplots(figsize=(15,12))
plt.axis('off')
plt.tight_layout(pad=0)
plt.imshow(img2)
ax.set_aspect('equal')
for output in outputs:
        r=output['right']
        l=output['left']
        t=output['top']
        b=output['bottom']
        rect = patches.Rectangle((l-4,t-3),r-l+8,b-t+4,linewidth=1,edgecolor='b',facecolor='none')      
        ax.add_patch(rect)
        ax.annotate(output['class'],(l-7,t-19),color='w',fontsize=16)
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0) 
plt.show()
