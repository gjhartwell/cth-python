# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 22:20:03 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from vmec import VMEC
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString


test = VMEC('test.nc')
R, Z =test.get_flux_surfaces_at_phi_cyl(26) 

R, Z = R[7],Z[7]


points = []
for i in range(0, len(R)):
    points.append( (R[i],Z[i]) )
    
    
    
#print(points[10])

poly = Polygon(points)
line = LineString([(1, 0),(0, .1)])


hits = list(poly.intersection(line).coords)

print(hits[0])
print(hits[0][1])

x = [hits[0][0], hits[1][0]]
y = [hits[0][1], hits[1][1]]

print(np.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2))

#plt.figure()
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([.55, .8])
plt.ylim([-.25, .25])
plt.plot(R,Z, 'k')
plt.plot([1, 0], [0, .1], 'r')
plt.scatter(x, y, c ='b')

plt.show()


