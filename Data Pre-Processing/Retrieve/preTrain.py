#Alex Fay 3/15/2020
import urllib.request
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from google.colab import files

#read csv file
file = "BrightGal16-17.csv" #change csv name as needed
df = pd.read_csv(file)

#getting image from each row and column
for i in df.index:
  for i in range(80000,500002):
    ra = df['ra'][i]
    dec = df['dec'][i]
    objID = df['objID'][i]

#SDSS Search Engine
    url ="http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?TaskName=Skyserver.Chart.List&ra=41.4488679045723&dec=" + str(ra) + "&dec=" + str(dec)
    imgName ="Bright:16-17+fileNum:" + str(i) + "+objID:" + str(objID) + ".jpg"

#Catch missing images and move on
    try:
        urllib.request.urlretrieve(url, imgName)
        print(i)
        files.download(imgName)
    except:
        print("Missing" + str(i))
