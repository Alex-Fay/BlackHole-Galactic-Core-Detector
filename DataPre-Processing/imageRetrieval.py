#@Author: Alex Fay 3/21/2020
import urllib.request
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

#read csv file
file = "Galaxy.csv"
df = pd.read_csv(file)

#getting image from each row and column
for i in df.index:
  for i in range(2,-1):
    ra = df['ra'][i]
    dec = df['dec'][i]

    url ="http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.List&ra=" + str(ra) + "&dec=" + str(dec)
    imgName = str(i) + ".jpg"
    urllib.request.urlretrieve(url, imgName)
