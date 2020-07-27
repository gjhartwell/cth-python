# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 11:51:37 2019

@author: Ellie_2
"""

# Values are stored within dicts. Both values and uncertainties are stored. 
# To access, for example, temperature. 

# Example usage:  data = triple_probe_manipulation.triple_probe_values(19081452)
# plt.plot(data['Time'],data['Electron Density']['Value'])

# Uncertainties for all values are saved under ['Uncertainty'] (as opposed to ['Value'])
    
import MDSplus as mds
import numpy as np
import scipy.signal as ss   
import supporting_functions as sf 
sm = 11  # smoothing parameter for the actual data
unc_sm = 101 # smoothing parameter for uncertainty calculation
charge = 1.60e-19 # Coulombs
area = 1.02e-5 #mm
ion_mass = 1.67e-27 # kg 
el_mass = 9.11e-31 # kg 
start_time = 1.50
end_time = 1.75

def triple_probe_sys_variables(shotnum):


    
    # Connecting to tree
    tree = 't' + str(shotnum)[0:6]
    conn = mds.connection.Connection('131.204.212.37')
    conn.openTree(tree, shotnum)
    
    # Importing all data
    system_variables = {}
    system_variables["Power time"] = conn.get('dim_of(\PWR_ECRH_KLY1_FWD)').data()
    system_variables["Power 1"] = conn.get('\PWR_ECRH_KLY1_FWD').data()[sf.nearby(system_variables["Power time"],start_time):sf.nearby(system_variables["Power time"],end_time)]
    system_variables["Power 3"] = conn.get('\PWR_ECRH_KLY3_FWD').data()[sf.nearby(system_variables["Power time"],start_time):sf.nearby(system_variables["Power time"],end_time)]
    
    system_variables["Power time"] = system_variables["Power time"][sf.nearby(system_variables["Power time"],start_time):sf.nearby(system_variables["Power time"],end_time)]
    
    system_variables["Total Power"] = system_variables["Power 3"] + system_variables["Power 1"]
    
    
    system_variables["Gas time"] = conn.get('dim_of(acq196:input_01)').data()
    system_variables["Gas"] = conn.get('acq196:input_65').data()[sf.nearby(system_variables["Gas time"],start_time):sf.nearby(system_variables["Gas time"],end_time)]/float(conn.get('acq1_com:ch65:gain'))
    system_variables["Gas time"] = system_variables["Gas time"][sf.nearby(system_variables["Gas time"],start_time):sf.nearby(system_variables["Gas time"],end_time)]
    
    system_variables["Gas"] = 1.86e15*np.exp(1.92*system_variables["Gas"])
    
    return system_variables
    
def triple_probe_values(shotnum):

    
#    import MDSplus as mds
#    import numpy as np
#    import scipy.signal as ss   
#    import supporting_functions as sf 
#    sm = 11  # smoothing parameter. 
#    unc_sm = 101
#    charge = 1.60e-19 # Coulombs
#    area = 1.02e-5 #mm
#    ion_mass = 1.67e-27 # kg 
#    el_mass = 9.11e-31 # kg 
#    start_time = 1.50
#    end_time = 1.75
    
    # Connecting to tree
    tree = 't' + str(shotnum)[0:6]
    conn = mds.connection.Connection('131.204.212.37')
    conn.openTree(tree, shotnum)
    
    
    # from cthconnect import cthconnect
    # from cthopen import cthopen
    
#    power
#   gas
#   probe variables: probe 1, floating potential, current, temperature, density, potential    
    
    tp_variables = {}
    
    tp_variables["Time"] = conn.get('dim_of(acq1962:input_01)').data()
    tp_variables["Probe 1"] = {}
    tp_variables["Probe 1"]["Value"] = conn.get('acq1962:input_44').data()[sf.nearby(tp_variables["Time"],start_time):sf.nearby(tp_variables["Time"],end_time)]/float(conn.get('acq2_com:ch44:gain'))
    tp_variables["Probe 1"]["Uncertainty"] = abs(tp_variables["Probe 1"]["Value"] - ss.savgol_filter(tp_variables["Probe 1"]["Value"],unc_sm,3))
    tp_variables["Probe 1"]["Value"] = ss.savgol_filter(tp_variables["Probe 1"]["Value"],sm,3)
    tp_variables["Floating Potential"] = {}
    tp_variables["Floating Potential"]["Value"] = conn.get('acq1962:input_45').data()[sf.nearby(tp_variables["Time"],start_time):sf.nearby(tp_variables["Time"],end_time)]/float(conn.get('acq2_com:ch45:gain'))
    tp_variables["Floating Potential"]["Uncertainty"] = abs(tp_variables["Floating Potential"]["Value"] - ss.savgol_filter(tp_variables["Floating Potential"]["Value"],unc_sm,3))
    tp_variables["Floating Potential"]["Value"] = ss.savgol_filter(tp_variables["Floating Potential"]["Value"],sm,3)
    tp_variables["Current"] = {}
    tp_variables["Current"]["Value"] = conn.get('acq1962:input_46').data()[sf.nearby(tp_variables["Time"],start_time):sf.nearby(tp_variables["Time"],end_time)]/float((100*conn.get('acq2_com:ch46:gain')))
    tp_variables["Current"]["Uncertainty"] = abs(tp_variables["Current"]["Value"] - ss.savgol_filter(tp_variables["Current"]["Value"],unc_sm,3))
    tp_variables["Current"]["Value"] = ss.savgol_filter(tp_variables["Current"]["Value"],sm,3)

    tp_variables["Time"] = tp_variables["Time"][sf.nearby(tp_variables["Time"],start_time):sf.nearby(tp_variables["Time"],end_time)]
    
    
    # power_1 = smooth(power_1,sm)
    # power_3 = smooth(power_3,sm)   
    
    # Manipulating data to be what we actually want
    consts = 1000*ion_mass**.5*np.exp(0.5)/(charge*area)
    tp_variables["Temperature"] = {}
    tp_variables["Temperature"]["Value"] = (tp_variables["Probe 1"]["Value"]-tp_variables["Floating Potential"]["Value"])/np.log(2)
    tp_variables["Temperature"]["Value"][np.where(tp_variables["Temperature"]["Value"] <= .01)] = .01
    tp_variables["Temperature"]["Uncertainty"] = np.sqrt((tp_variables["Probe 1"]["Uncertainty"]**2+tp_variables["Floating Potential"]["Uncertainty"]**2)/(np.log(2)**2))
    tp_variables["Electron Density"] = {}
    tp_variables["Electron Density"]["Value"] = (tp_variables["Current"]["Value"]/(charge*area))*(abs(ion_mass/(tp_variables["Temperature"]["Value"]*charge))**.5)*np.exp(0.5)
    tp_variables["Electron Density"]["Uncertainty"] = np.sqrt(consts**2*tp_variables["Current"]["Uncertainty"]**2/tp_variables["Temperature"]["Uncertainty"] + (consts*tp_variables["Current"]["Value"])**2*tp_variables["Temperature"]["Uncertainty"]**2/(4*tp_variables["Temperature"]["Value"]**3))
    tp_variables["Plasma Potential"] = {}
    tp_variables["Plasma Potential"]["Value"] = (tp_variables["Temperature"]["Value"]/2)*(np.log(ion_mass/(2*np.pi*el_mass))+1) + tp_variables["Floating Potential"]["Value"]
    tp_variables["Plasma Potential"]["Uncertainty"] = (tp_variables["Temperature"]["Uncertainty"]/2)*(np.log(el_mass/(2*np.pi*ion_mass))+1) + tp_variables["Floating Potential"]["Uncertainty"]  
    
    
    return tp_variables