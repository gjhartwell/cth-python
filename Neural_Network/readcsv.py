# --------------------------------------
# readcsv.py
# 
# reads a csv file and puts data into an array
#
# 	This routine assumes that the CSV file has the header:
#	HF	TVF	OH	SVF	TF	IP	PHIEDGE
#
# Returns: the array of data (less the header)
#
# Example: myarray=readcsv()
#       
#
# Also defines: nothing
#
# To do:
#	generalize to any file name
#	
# Greg Hartwell
# 2017-10-31
#----------------------------------------------------------------------------
import csv
import numpy as np

def readcsv():
	with open('mattsdata1.csv',"rb") as ifile:
		reader=csv.reader(ifile)
		# count the number of rows to set the array size
		# assumes that we have 7 columns 		
		irows=sum(1 for row in reader)
		array=np.empty([irows-1,7],dtype=float)
		# reset the row counter
		ifile.seek(0)

		irow=0
		for row in reader:
			if irow== 0:
				header=row
			else:
				icol=0
				for ir in row:
					data=float(ir)
					array[irow-1,icol]=data
					icol += 1
			irow +=1
		ifile.close()
	print "finished reading CSV file"
	print "There are ",irows-1,"rows of data"
	print "Array size is ",np.shape(array)
	return array
