# -*- coding: utf-8 -*-
# --------------------------------------
# tree_from_shot.py
# 
# MDSplus Python project
# for CTH data access
#
# 	tree_from_shot --- returns the CTH MDSplus tree associated with the 
#                   given shot number
#
# Parameters:
#	shotnum - integer - the shotnumber to open
# Returns:
#	tree - the cth tree for shotnum
#
# Example:
#       mytree=tree_from_shot(shotnum)
#
# 
#	
# Greg Hartwell
# 2016-12-16
#------------------

def tree_from_shot(shotnum):
	shotString=str(shotnum)
	tree= 't'+shotString[0:6]
	return tree
#-----------------------------------------------------------------------------