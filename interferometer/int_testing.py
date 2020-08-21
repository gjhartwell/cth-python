# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 08:42:06 2020

@author: hartwgj
"""

#from interferometer_processing import CTHintfrm_1mm
import scipy.constants
from scipy import fft,ifft
from cthmds import CTHData
import numpy as np


def getintdata(shotnum,chord):
    
    sawtooth_ch=[(5,1),(5,1),(5,1),(6,2)]
    data_ch = [(5,2),(5,3),(5,4),(6,3)]
    
    intsig=CTHData('intgis')
    sawsig=CTHData('intsaw')
    sawsig.get_data(server='mds',shotnum=shotnum,board_channel=sawtooth_ch[chord-1])
    intsig.get_data(server='mds',shotnum=shotnum,board_channel=data_ch[chord-1])
    
    return sawsig,intsig

#testing

# shotnum=20063020
# chord=1
# debug=1
# #CTHintfrm_1mm(shotnum,chord,debug)

# sawsig,intsig=getintdata(shotnum,chord)
