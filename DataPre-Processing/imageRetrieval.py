#@Author: Alex Fay 3/21/2020import urllib.request
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from google.colab import files

#read csv file
file = "Galaxy.csv"
df = pd.read_csv(file)

#getting image from each row and column
for i in df.index:
  for i in range(2,500002):
    ra = df['ra'][i]
    dec = df['dec'][i]
    objID = df['objID'][i]

    url ="http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.List&ra=" + str(ra) + "&dec=" + str(dec)
    imgName = "Gal+fileNum:" + str(i) + "+objID:" + str(objID) + ".jpg"
    
 #download each image if data exists
    try:
        urllib.request.urlretrieve(url, imgName)
        print(i)
        files.download(imgName)
    except:
        print("Missing" + str(i))
