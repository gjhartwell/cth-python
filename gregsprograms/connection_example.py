# MDSplus python test program

from MDSplus import Connection
c=Connection("mds.physics.auburn.edu:8000")
c.openTree('t161205',16120520)
c.closeTree
strayrf=c.get('\stray_rf')
print c.get('getenv("MDS_PATH")')

