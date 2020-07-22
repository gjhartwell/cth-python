import numpy as np
import xarray as ncdata
import matplotlib.pyplot as plt
from mayavi import mlab # to overrid plt.mlab
from surface import *
import os
cwd = os.getcwd()
name = cwd + "/wout_vmec.nc"
#x, y , z = plot_vmec_surface(name,plottype='surface3d')
plot_vmec_surface(name,plottype='cross-section',zeta=360)
