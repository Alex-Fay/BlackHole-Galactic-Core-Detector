#@Alex Fay: Polynomial Regression 5/1/2020-5/3/2020
#credit to Nhan Tran for sklearn Polynomial tutorial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Importing data
col = []
for i in range(300): col.append(str(i))
dataset = pd.read_csv("Spiral_radial.csv")
x = dataset[col].values #radius pixel and theta 
y = dataset.iloc[0, 1: -2].values #pixel radius
x = x.reshape((300, 18075)) 
y = y.reshape((300, 1)) #required for singular row in sklearn

#Split Data
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0) #25 percent data for testing

# Fitting Polynomial Regression
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree= 5)
X_poly = poly_reg.fit_transform(x)
poly_reg.fit(X_poly, y)

# Plot
def viz_polymonial():
    plt.scatter(x, y, color='red')
    plt.plot(X, pol_reg.predict(poly_reg.fit_transform(x)), color='blue')
    plt.title("Average Radial Light Fit: Spiral Galaxy")
    plt.xlabel("Pixel Radius")
    plt.ylabel("Luminosity")
    plt.show()
    return
viz_polymonial()

# Predicting a new result with Polymonial Regression
pol_reg.predict(poly_reg.fit_transform([[5.5]]))
