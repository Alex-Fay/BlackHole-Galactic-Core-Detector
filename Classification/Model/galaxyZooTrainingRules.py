#Alex Fay 4/2-10/2020 Code needs to be cleaned, 4am results but it runs and it's right :/

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from google.colab import files
import numpy as np

#=============Importing CSV and coloumns==============
#read csv file
file = "training_solutions_rev1.csv" #Galaxy Zoo Survey percents https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge/overview/the-galaxy-zoo-decision-tree
df = pd.read_csv(file)

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

label = []

def elliptical(i):
  isEllipse = True
  if(smooth[i] > disk[i]):
    if((roundness[i] > longAndSkinny[i]) | (semiRound[i] > longAndSkinny[i])): #Elliptical Types: E0- E3
      if(notOdd[i] > odd[i]):
        label.append("Elliptical")
        print("Elliptical")
    else:
      label.append("Elliptical Cigar") #E4-E7
      print("Cigar E")
  else:
    isEllipse = False
  return isEllipse

def spiral(i):
  booly = True
  if(disk[i] > smooth[i]): #Q1
    if(edgeOn[i] > notOnEdge[i]): #Q2
      if((boxy[i] < centerRound[i]) | (boxy[i] < centerNoBulge[i])):#Q9
        if(notOdd[i] > odd[i]): 
          label.append("Spiral")
          print("Spiral")
        elif((ring[i] > disturbed[i])): #check irregular
          label.append("Spiral")
          print("Spiral")
        elif(lensOrArc[i] > irregular[i]):
          label.append("Spiral")
          print("Spiral")
        else: 
          booly = False
      elif(bar[i] > noBar[i]): #boxy galaxy with bar
        if(notOdd[i] > odd[i]):
           label.append("Bar Spiral")
           print("Bar Spiral")
        elif((ring[i] > disturbed[i]) | (lensOrArc[i] > irregular[i])):
           label.append("Bar Spiral")
           print("Ba Spiral")
        else:
          booly = False
      else:
        booly = False
    else:
      if(noBar[i] > bar[i]):
        if(spiralArmPresent[i] > noSpiralArm[i]):
           label.append("Spiral")
           print("Spiral")
        else: 
          booly = False
      else:
        if(notOdd[i] > odd[i]):
           label.append("Bar Spiral")
           print("Bar Spiral")
        elif((ring[i] + lensOrArc[i]) > (disturbed[i] + irregular[i])):
           label.append("Bar Spiral")
           print("Bar Spiral")
        else:
          booly = False
  return booly

def lenticular(i):
  isLenticular = True
  if(disk[i] > smooth[i]):
    if(notOnEdge[i] > edgeOn[i]):
      if(noBar[i] > bar[i]):
        if(noSpiralArm[i] > spiralArmPresent[i]):
          if((noBulge[i] + someBulge[i]) < (obviousBulge[i] + dominantBulge[i])):
            if(notOdd[i] > odd[i]):
               label.append("Lenticular")
               print("Lenticular")
    else:
      if(noBulge[i] < .25):
        if(noSpiralArm[i] > spiralArmPresent[i]):
          if(notOdd[i] > odd[i]):
             label.append("Lenticular")
             print("Lenticular")
  else:
    isLenticular = False
  return isLenticular

#========Main==========
for i in df.index & range(0, 61578):
  if ((star[i] > disk[i]) & (star[i] > smooth[i])):
     label.append('STAR')
  else:
    if (elliptical(i) == False):
      if(spiral(i) == False):
        if(lenticular(i) == False ):
           label.append("Irregular")
           print("Irregular")

#add values to csv
print(label)
ndf = pd.DataFrame(list(zip(label)))
ndf.to_csv("results.csv")
#df.to_csv("training_solutions_rev1.csv")