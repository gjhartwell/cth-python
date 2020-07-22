# --------------------------------------
# cthconnect.py
# 
# MDSplus Python project
# for CTH data access
#
# cthconnect connects to the neil or mds database locations
#
# Parameters:
#	server - either the mds.physics.auburn.edu	
#	                   or 131.204.212.32 (neil)
#                  default is mds
# Return: a connection
#
# Example:
#       connection = cthconnect(server)
#       connection = cthconnect()
#
# Greg Hartwell
# 2016-12-6
#----------------------------------------------------------------------------

from cthconnect import cthconnect
from cthopen import *
from MDSplus import *
from timeSubset import timeSubset

c=cthconnect(server="mds")
shotnum=16120630
tree=treeFromShot(shotnum)
c.openTree(tree,shotnum)
data=c.getNode('\I_p').data()
shot=c.get('$shot')
print shot


import pylab as pl
import numpy
import matplotlib

pl.plot(data)
pl.show()


#tree = treeFromShot(15100312)
#print tree


