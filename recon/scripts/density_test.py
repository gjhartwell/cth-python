# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:31:26 2020

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from v3fit_database import ReconResults
import matplotlib.pyplot as plt

shot = 20020515

query= "SELECT * FROM results WHERE shot=?"
r1 = ReconResults(query,  (int(shot),))
r1.select_results(query, (int(shot),))

print(r1.raw_density)