# --------------------------------------
# arraytodata.py
# 
# converts data read from CSV file to format usable by scikit-learn modules
#
# 	This routine assumes that the CSV file has the header:
#	HF	TVF	OH	SVF	TF	IP	PHIEDGE
#
# Returns: a named tuple with the first 6 columns as data and phiedge as target
#
# Example: mydata=arraytodata(array)
#       
#
# Also defines: nothing
#
# To do:
#	
#	
# Greg Hartwell
# 2017-11-1
#----------------------------------------------------------------------------

import numpy as np
import collections

def arraytodata(array):
	size=np.shape(array)
#	print "array shape is ",size
#	print "number of rows is :",size[0]
#	print "number of columns is :",size[1]
	rows=size[0]
	cols=size[1]

	mydata=array[0:rows,0:6]
	mytarget=array[0:rows,6]

#	print "data array shape is ",np.shape(data)
#	print "target array shape is ",np.shape(target)

	nndata=collections.namedtuple('nndata',['data','target'])
	mattdata=nndata(data=mydata,target=mytarget)
	return mattdata


