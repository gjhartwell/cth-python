# --------------------------------------
# LRtest.py
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
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

tindex=500
rerr=50
amp=.001
x=np.arange(0,1000).reshape(-1,1)
y=x*amp
err=(np.random.rand(1000)-0.5)*rerr*2.0*amp
err=err.reshape(-1,1)
y=y+err
y=np.ravel(y)

plt.figure(1)
plt.scatter(x,y,s=.1)
plt.xlabel('x')
plt.ylabel('y',)
plt.title('Data')

nndata=collections.namedtuple('nndata',['data','target'])
mydata=nndata(data=x,target=y)

x_train=mydata.data[:tindex]
x_test=mydata.data[tindex:]

print np.shape(x_train)

y_train=mydata.target[:tindex]
y_test=mydata.target[tindex:]


print np.shape(y_train)

## Create linear regression object
regr = linear_model.LinearRegression()
regr.fit(x_train, y_train)
y_pred=regr.predict(x_test)
train_y_pred=regr.predict(x_train)

## The coefficients
print('Coefficients: \n', regr.coef_)
print("Train Mean squared error: %.2f" 
      % mean_squared_error(y_train, train_y_pred))
print("Test Mean squared error: %.2f" 
      % mean_squared_error(y_test, y_pred))
## Explained variance score: 1 is perfect prediction
print('Train Variance score: %.2f' % r2_score(y_train, train_y_pred))
print('Test Variance score: %.2f' % r2_score(y_test, y_pred))
vs=r2_score(y_test, y_pred)

## Plot outputs
plt.figure(2)
plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, y_pred, color='blue', linewidth=3)
varstring="variance score= %.2f" % vs
#plt.text(950,990,varstring)

plt.show()


