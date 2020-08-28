# --------------------------------------
# mlptest.py
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

tindex=950
rerr=0
x=np.arange(0,1000).reshape(-1,1)
y=x*1.0
err=(np.random.rand(1000)-0.5)*rerr*2.0
err=err.reshape(-1,1)
y=y+err
y=np.ravel(y)

plt.figure(1)
plt.scatter(x,y,s=.1)
plt.xlabel('x')
plt.ylabel('y',)
plt.title('Data')
#plt.show()

nndata=collections.namedtuple('nndata',['data','target'])
mydata=nndata(data=x,target=y)

from sklearn import neural_network
from sklearn.metrics import mean_squared_error, r2_score

## Load the diabetes dataset
#diabetes = datasets.load_diabetes()

## Use only one feature
#diabetes_X = diabetes.data[:, np.newaxis, 2]

## Split the data into training/testing sets
#diabetes_X_train = diabetes_X[:-20]
#diabetes_X_test = diabetes_X[-20:]

x_train=mydata.data[:tindex]
x_test=mydata.data[tindex:]

print np.shape(x_train)

## Split the targets into training/testing sets
#diabetes_y_train = diabetes.target[:-20]
#diabetes_y_test = diabetes.target[-20:]

y_train=mydata.target[:tindex]
y_test=mydata.target[tindex:]


print np.shape(y_train)

## Create linear regression object
mlp = neural_network.MLPRegressor()
mlp.set_params(learning_rate_init= .01,verbose=True,tol=.0001)

print("----------------parameters---------------")
params=mlp.get_params()
for key, value in params.items():
	print key,value



## Train the model using the training sets
#regr.fit(diabetes_X_train, diabetes_y_train)
print('-------------Training----------------')
mlp.fit(x_train, y_train)


## Make predictions using the testing set
#diabetes_y_pred = regr.predict(diabetes_X_test)
y_pred=mlp.predict(x_test)

y_pred_train=mlp.predict(x_train)
plt.figure(2)
plt.scatter(y_train,y_pred_train,s=.1)
plt.xlabel('y_train')
plt.ylabel('y_predicted',)
plt.title('Training data prediction')

## The coefficients
#print('Coefficients: \n', regr.coef_)
## The mean squared error
#print("Mean squared error: %.2f"
#      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
print("-----------Results------------")
print "Loss ",mlp.loss_
print "Iterations ",mlp.n_iter_
print "Outputs ",mlp.n_outputs_
print "Output Name ",mlp.out_activation_
#print "Coefs ", mlp.coefs_
#print "Intercepts ",mlp.intercepts_ 
print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
## Explained variance score: 1 is perfect prediction
#print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))
print('Variance score: %.2f' % r2_score(y_test, y_pred))
print('The test score is',mlp.score(x_test,y_test))
print('The training score is',mlp.score(x_train,y_train))

## Plot outputs
plt.figure(4)
plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, y_pred, color='blue', linewidth=3)
plt.title('Model Testing')

#plt.show()


