# --------------------------------------
# timeSubset.py
# 
# MDSplus Python project
# for CTH data access
#
# 	timeSubset --- returns the subset of an array between given times 
#
# Parameters:
#	taxis- the time axis that tInit and tFinal reference
#	data - the array to take the time subset of
#	tInit - the initial time
#	tFinal - the final time
# Returns:
#	the subset of the data array between times tInit and tFinal
#
# Example:
#       shortTaxis  = timeSubset(taxis,taxis,1.6,1.7)
#       shortData   = timeSubset(taxis,data,1.6,1.7)
#
# Also defines: testTimeSubset() to test the routine
#	
#
# 
# Greg Hartwell
# 2016-12-20
# 
# last modifies 2017-10-27 to fix the code
#----------------------------------------------------------------------------
from numpy import extract
from numpy import arange
import matplotlib.pyplot as plt

# this is a test program for the timeSubset routine
def testTimeSubset():
    time=arange(0,1000,.1)
    t2=timeSubset(time,time,200,400)
    plt.plot(t2)
    plt.show()
    
 
def timeSubset(taxis,data,tInit,tFinal):

    #create a temp array for times greater than t1
    #then create the final array from the temp array for
    #times less than t2 
	condition1 = (taxis >= tInit)
	nt1=extract(condition1,taxis)
	condition2 = (nt1 <= tFinal)
	newdata=extract(condition1,data)
	newdata2=extract(condition2,newdata)
	
	return newdata2
# ---------------------------------------------------------------------------
