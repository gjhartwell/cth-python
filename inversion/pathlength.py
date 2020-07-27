# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 22:51:45 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from vmec import wout_file
import numpy as np
from shapely.geometry import Polygon, LineString

# =============================================================================
# Purpose: Pathlength class to find the pathlengths associated for a vector
# going through the respective flux surfaces. This will allow a inversion to be
# done.
# 
# To Do: Carry this through to inversion
# 
# =============================================================================


class Pathlength2D:
    
    def __init__(self, R, Z):
        self.R = R[1:]
        self.Z = Z[1:]
        
        self.points_tuple = self.points_R_Z_array_to_tuple(self.R, self.Z)
    
    
    def single_pathlength(self, line_point1, line_point2):
        #line defined by two points (both points outside flux surface)
        
        line_point1 = self.array_to_tuple(line_point1)
        line_point2 = self.array_to_tuple(line_point2)      
        
        f_n_max = len(self.R)
        line = LineString([line_point1, line_point2])
        
        pathlengths_r = []
        pathlengths_c = []
        
        poly = Polygon(self.points_tuple[0])


        if poly.intersects(line):
            coords = list(poly.intersection(line).coords)
            length = self.distance_between_intersection_coords(coords)
            pathlengths_r.append(length)
            pathlengths_c.append(length)
        else:
            pathlengths_r.append(0)
            pathlengths_c.append(0)
            
        for i in range(1, f_n_max):
            poly = Polygon(self.points_tuple[i])
            #running_length = pathlengths[0]
            
            if poly.intersects(line):
                coords = list(poly.intersection(line).coords)
                length = self.distance_between_intersection_coords(coords)
 
                pathlengths_r.append(length)
                length = length - pathlengths_r[i - 1]

                pathlengths_c.append(length)
            else:
                pathlengths_r.append(0)
                pathlengths_c.append(0)
       
        
        return pathlengths_c
        #return coords


    def outersect(self, line_point1, line_point2):
        #line defined by two points (both points outside flux surface)
        
        line_point1 = self.array_to_tuple(line_point1)
        line_point2 = self.array_to_tuple(line_point2)      
        
        f_n_max = len(self.R)
    
        
        line = LineString([line_point1, line_point2])
        
        pathlengths_r = []
        pathlengths_c = []
        
        #print(f_n_max)
        
        poly = Polygon(self.points_tuple[f_n_max-1])


        if poly.intersects(line):
            coords = list(poly.intersection(line).coords)
            length = self.distance_between_intersection_coords(coords)
            pathlengths_r.append(length)
            pathlengths_c.append(length)
        else:
            coords = None
            pathlengths_r.append(0)
            pathlengths_c.append(0)
            
        #return pathlengths_c,coords
        return coords
   
    
    def multi_pathlength(self, line_points):
        # line_points = [[line1_point1, line1_point2],[line2_point1, line2_point2]]
        
        pathlength_matrix = []
        
        for i in range(0, len(line_points)):
            point1 = line_points[i][0]
            point2 = line_points[i][1]
            
            length = self.single_pathlength(point1, point2)
            pathlength_matrix.append(length)
            
        return pathlength_matrix
            
    
    def distance_between_intersection_coords(self, coords):
        hits = coords
        x = [hits[0][0], hits[1][0]]
        y = [hits[0][1], hits[1][1]]
    
        length = np.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2)
        
        return length
    
    
    def array_to_tuple(self, point):
        # point in array to point in tuple
        new_point = (point[0], point[1])
        return new_point

    
    def points_R_Z_array_to_tuple(self, R, Z):
        points = []
        
        for i in range(0, len(R)):
            subpoints = []
            for j in range(0, len(R[i])):
                #print(i,j)
                #print(R[i][j])
                subpoints.append( (R[i][j], Z[i][j]))
                
            points.append(subpoints)
            
        return points
    
    
    
"""    
test = VMEC('test.nc')
R, Z  = test.get_flux_surfaces_at_phi_cyl(26)    

test = Pathlength2D(R, Z)




points = [[(1, 0), (0, .3)], [(1, .1), (0, .1)]]

y = test.multi_pathlength(points)

print(sum(y[0]))
print(sum(y[1]))
"""

