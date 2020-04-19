#Alex Fay 4/2-10/2020  Update: 4/19
#Notes: some repeat if statements could be split into sub tests i.e. isBoxy(), AddLabel(str), isIrregular()
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from google.colab import files
import numpy as np

#=============Importing CSV and coloumns==============
#read csv file
file = "training_solutions_rev1.csv" #Galaxy Zoo Survey percents https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/overview/the-galaxy-zoo-decision-tree
df = pd.read_csv(file)

#Labeling Images
imgName = df["GalaxyID"]

#Q1 Is galaxy smooth, round, or no disk
smooth = df['Class1.1']
disk = df['Class1.2']
star = df['Class1.3']

#Q2 is disk on edge
edgeOn = df['Class2.1']
notOnEdge = df['Class2.2']

#Q3 is bar of galaxy present
bar = df['Class3.1']
noBar = df['Class3.2']

#Q4 spiral arm patter present
spiralArmPresent = df['Class4.1']
noSpiralArm = df['Class4.2']

#Q5 central bulge
noBulge = df['Class5.1']
someBulge = df['Class5.2']
obviousBulge = df['Class5.3']
dominantBulge = df['Class5.4']

#Q6 odd image
odd = df['Class6.1']
notOdd = df['Class6.2']

#Q7 roundness
roundness = df['Class7.1']
semiRound = df['Class7.2']
longAndSkinny = df['Class7.3']

#Q8 ring
ring = df['Class8.1']
lensOrArc = df['Class8.2']
disturbed = df['Class8.3']
irregular = df['Class8.4']

#Q9
centerRound = df['Class9.1']
boxy = df['Class9.2']
centerNoBulge = df['Class9.3']

#Q10
tight = df['Class10.1']
medium = df['Class10.2']
loose = df['Class10.3']

#Q11
oneArm = df['Class11.1']
twoArms = df['Class11.2']
threeArms = df['Class11.3']
fourArms = df['Class11.4']
manyArms = df['Class11.5']
unknownArms = df['Class11.6']

#arrays for adding to csv at end
label = []
pictureNames = []

#===========Tests for each galaxy type===========
def elliptical(i): #tests for Elliptical Cigar, elliptical normal, or none
  isEllipse = True
  if(smooth[i] > disk[i]):
    if((roundness[i] > longAndSkinny[i]) | (semiRound[i] > longAndSkinny[i])): #Elliptical Types: E0- E3
      if(notOdd[i] > odd[i]): #checks for irregular properties
        label.append("Elliptical")
        pictureNames.append((str(imgName[i]) + ".jpg"))
        print("Elliptical")
      else:
        isEllipse = False
    else:
      label.append("Elliptical Cigar") #E4-E7 galaxy types (see Hubble picture)
      pictureNames.append((str(imgName[i]) + ".jpg"))
      print("Cigar E")
  else:
    isEllipse = False
  return isEllipse

def spiral(i): #tests if Spiral, Spiral w/ Bar, or not Spiral
  isSpiral = True
  if(disk[i] > smooth[i]):   #------All Spiral Galaxies have disk feature----
  #==========edge function splits into 2 seperate classification tests=========
    if(edgeOn[i] > notOnEdge[i]):
      if((boxy[i] < centerRound[i]) | (boxy[i] < centerNoBulge[i])): #Q9
      #----Irregular Tests-------
        if(notOdd[i] > odd[i]): #Irregular Test
          label.append("Spiral")
          pictureNames.append((str(imgName[i]) + ".jpg"))
          print("Spiral")
        elif(ring[i] > disturbed[i]): #pull rings from not irregular
          label.append("Spiral")
          pictureNames.append((str(imgName[i]) + ".jpg"))
          print("Spiral")
        elif(lensOrArc[i] > irregular[i]): #pull lens from irregular
          label.append("Spiral")
          pictureNames.append((str(imgName[i]) + ".jpg"))
          print("Spiral")
        else: 
          isSpiral = False
      #----Test for Galaxy is Barred-----
      elif(bar[i] > noBar[i]):
        #----Irregular Tests----
        if(notOdd[i] > odd[i]):
           label.append("Bar Spiral")
           pictureNames.append((str(imgName[i]) + ".jpg"))
           print("Bar Spiral")
        elif((ring[i] > disturbed[i]) | (lensOrArc[i] > irregular[i])): #pull spiral abnormal irregular properties
           label.append("Bar Spiral")
           pictureNames.append((str(imgName[i]) + ".jpg"))
           print("Ba Spiral")
        else:
          isSpiral = False
      else:
        isSpiral = False #not disk
    #====Q2 if not On edge/ sideways======
    else:
      #-------Test if Barred---------
      if(noBar[i] > bar[i]):
        if(spiralArmPresent[i] > noSpiralArm[i]):
           label.append("Spiral")
           pictureNames.append((str(imgName[i]) + ".jpg"))
           print("Spiral")
        else: 
          isSpiral = False
      else:
        #--------Irregular Tests--------
        if(notOdd[i] > odd[i]):
           label.append("Bar Spiral")
           pictureNames.append((str(imgName[i]) + ".jpg"))
           print("Bar Spiral")
        elif((ring[i] + lensOrArc[i]) > (disturbed[i] + irregular[i])):
           label.append("Bar Spiral")
           pictureNames.append((str(imgName[i]) + ".jpg"))
           print("Bar Spiral")
        else:
          isSpiral = False
  else:
    isSpiral = False #catch all else
  return isSpiral

def lenticular(i):
  isLenticular = True
  if(disk[i] > smooth[i]): #all lenticular are disks
  #-----seperate edge tests, seperate process-----
    if(notOnEdge[i] > edgeOn[i]):
      if(noBar[i] > bar[i]):
        if(noSpiralArm[i] > spiralArmPresent[i]): #spiral arms only charecteristic of spirals
          if((noBulge[i] + someBulge[i]) < (obviousBulge[i] + dominantBulge[i])):
            #----Irregular Test----
            if(notOdd[i] > odd[i]):
               label.append("Lenticular")
               pictureNames.append((str(imgName[i]) + ".jpg"))
               print("Lenticular")
            else:
              isLenticular = False
          else:
            isLenticular = False #Bulge Failed
        else:
          isLenticular = False #spiral test failed
      else:
        isLenticular = False #bar failed
  #----2nd case for edge, edge = True-------
    else:
      if(noBulge[i] < .25):
        if(noSpiralArm[i] > spiralArmPresent[i]):
          if(notOdd[i] > odd[i]):
             label.append("Lenticular")
             pictureNames.append((str(imgName[i]) + ".jpg"))
             print("Lenticular")
          else:
            isLenticular = False #irregular
        else:
          isLenticular = False #spiral arm test
      else:
        isLenticular = False #Bulge
  else:
    isLenticular = False
  return isLenticular

#========Main==========
for i in df.index & range(0, 61578):
  if ((star[i] > disk[i]) & (star[i] > smooth[i])):
     label.append('STAR')
     pictureNames.append((str(imgName[i]) + ".jpg"))
  else:
    if (elliptical(i) == False):
      if(spiral(i) == False):
        if(lenticular(i) == False ):
           label.append("Irregular")
           pictureNames.append((str(imgName[i]) + ".jpg"))
           print("Irregular")

#add values to csv
print(label)
ndf = pd.DataFrame(list(zip(label, pictureNames)))
ndf.to_csv("HubbleImageLabels.csv")
