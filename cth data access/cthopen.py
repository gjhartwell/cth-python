# --------------------------------------
# cthopen.py
# 
# MDSplus Python project
# for CTH data access
#
# 	cthopen --- handles the opening of the shotnumber  
#
# Parameters:
#	connection - the connection handle
#	shotnum - integer - the shotnumber to open
# Returns:
#	none
#
# Example:
#       cthopen(conn,16120510)
#
# Also defines:
#	treeFromShot --- creates a tree name from the shot number
#	Parameter:
#		shotnum - integer - the shotnumber to open
#	Return:
#
# 
# Greg Hartwell
# 2016-12-6
#----------------------------------------------------------------------------
from MDSplus import Connection

def cthopen(connection,shotnum):
	tree=treeFromShot(shotnum)
	connection.openTree(tree,shotnum)
	

def treeFromShot(shotnum):
	shotString=str(shotnum)
	tree= 't'+shotString[0:6]
	return tree
# ---------------------------------------------------------------------------
