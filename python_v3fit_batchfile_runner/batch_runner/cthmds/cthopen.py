# -*- coding: utf-8 -*-
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
#	shotnum - an integer - the shotnumber to open
# Returns:
#	none
#
# Example:
#       cthopen(conn,16120510)
#
# 
# Greg Hartwell
# 2016-12-6
# 2017-12-13 -moved treeFromShot to separate file
#----------------------------------------------------------------------------

from tree_from_shot import tree_from_shot

def cthopen(connection,shotnum):
    tree=tree_from_shot(shotnum)
    connection.openTree(tree,shotnum)
    return connection

# ---------------------------------------------------------------------------
