# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 22:51:45 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from vmec import VMEC
import numpy as np
from shapely.geometry import Polygon, LineString

# =============================================================================
# Purpose: Pathlength class to find the pathlengths associated for a vector
# going through the respective flux surfaces. This will allow a inversion to be
# done.
# 
# To Do: Finish single_pathlength and apply it for a set of viewing chords
# 
# =============================================================================


class Pathlength:
    
    def __init__(self, vmec_R_Z, s):
        self.R = vmec_R_Z[0]
        self.Z = vmec_R_Z[0]
        self.s = s
    

    
    def single_pathlength(vector):
