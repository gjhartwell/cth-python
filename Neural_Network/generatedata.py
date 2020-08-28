# --------------------------------------
# generatedata.py
# 
# creates a data set for use in the nn routines
#
# 
#	
#	
# Greg Hartwell
# 2017-11-1
#----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import collections

x=np.arange(0,1000).reshape(-1,1)
y=x/1000.0
err=(np.random.rand(1000)-0.5)/100.0
err=err.reshape(-1,1)
y=y+err


plt.scatter(x,y,s=.1)
plt.xlabel('x (s)')
plt.ylabel('y (mV)',)
plt.title('Sample Data')
plt.show()

nndata=collections.namedtuple('nndata',['data','target'])
mydata=nndata(data=x,target=y)


from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

## Load the diabetes dataset
#diabetes = datasets.load_diabetes()

## Use only one feature
#diabetes_X = diabetes.data[:, np.newaxis, 2]

## Split the data into training/testing sets
#diabetes_X_train = diabetes_X[:-20]
#diabetes_X_test = diabetes_X[-20:]

x_train=mydata.data[:900]
x_test=mydata.data[900:]

print np.shape(x_train)

## Split the targets into training/testing sets
#diabetes_y_train = diabetes.target[:-20]
#diabetes_y_test = diabetes.target[-20:]

y_train=mydata.target[:900]
y_test=mydata.target[900:]

print np.shape(y_train)

## Create linear regression object
regr = linear_model.LinearRegression()

## Train the model using the training sets
#regr.fit(diabetes_X_train, diabetes_y_train)
regr.fit(x_train, y_train)
## Make predictions using the testing set
#diabetes_y_pred = regr.predict(diabetes_X_test)
y_pred=regr.predict(x_test)

## The coefficients
print('Coefficients: \n', regr.coef_)
## The mean squared error
#print("Mean squared error: %.2f"
#      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
## Explained variance score: 1 is perfect prediction
#print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))
print('Variance score: %.2f' % r2_score(y_test, y_pred))
## Plot outputs
plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, y_pred, color='blue', linewidth=3)

plt.show()


