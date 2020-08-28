# --------------------------------------
# getdata.py
# 
# wrapper program to: 	readcsv data 
#			convert it to a data type usable by the neural network program
#
# To do:
#	
#	
# Greg Hartwell
# 2017-11-1
#----------------------------------------------------------------------------

from readcsv import readcsv
from arraytodata import arraytodata

def getdata():
	array=readcsv()
	mydata=arraytodata(array)



