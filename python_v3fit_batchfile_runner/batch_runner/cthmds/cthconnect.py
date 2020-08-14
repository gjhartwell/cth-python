# -*- coding: utf-8 -*-
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
#	                 or 131.204.212.32 (neil)
#          defaults to the mds
# Return: an MDSplus connection
#
# Example:
#       connection = cthconnect(server)
#       connection = cthconnect()
#
# Greg Hartwell
# 2016-12-6
#----------------------------------------------------------------------------

from MDSplus import Connection

def cthconnect( server = "mds.physics.auburn.edu:8000" ):
	if server.lower() == "neil":
		server="10.168.7.208:8000"
	elif ((server == "mds") or (server == "mds.physics.auburn.edu")):
		server = "mds.physics.auburn.edu:8000"
	else:
		server = "mds.physics.auburn.edu:8000"

	connection=Connection(server)
	return connection

# END of cthconnect definition
#----------------------------------------------------------------------------
#from MDSplus import Connection

#def cthconnect( server = "mds.physics.auburn.edu:8000" ):
#	if server.lower() == "neil":
#		server="131.204.212.37:8000"
#	elif ((server == "mds") or (server == "mds.physics.auburn.edu")):
#		server = "mds.physics.auburn.edu:8000"
#	else:
#		server = "mds.physics.auburn.edu:8000"

#	connection=Connection(server)
#	return connection

# END of cthconnect definition
