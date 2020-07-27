# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:45:49 2018

@author: James
"""
import numpy as np
import matplotlib.pyplot as plt



exp_val = {} # dictionary of experimental values

exp_val['anisotropy'] = (0.395 *10**-82) / (8.8541878176*10**-12)**2
# the molecular - polarizability anisotropy for N2 in cm^6. 
# Value taken from M. J. van de Sande "Laser scattering on low 
# temperature plasmas: high resolution and stray light rejection" 2002
exp_val['N2_rot_constant'] = 199.887
# rotational constant for N2 molecule 
# This value was taken from C.M. Penney 
# "Absolute rotational Raman corss sections for N2, O2, and CO2" 1974
exp_val['h'] = 6.62607004*10**-34   # Planck_constant
exp_val['e'] = 1.60217662*10**-19
exp_val['me']= 9.10938356*10**-31   # mass of electron in kg
exp_val['epsilon'] = 8.8541878176*(10**-12) 
exp_val['c'] = 299792458            # speed of light
exp_val['kB'] = 1.38064852*10**-23  # Boltzmann constant m^2 kg s^-2 K^-1
exp_val['laser_wavelength'] = 532.0 *10**-9
exp_val['electron_radius**2'] = (((exp_val['e'])**2)/(4*np.pi*exp_val['epsilon'] *
                                  exp_val['me']*exp_val['c']**2))**2 * 10**4
exp_val['theta1'] = 86.371 * (np.pi/180)
exp_val['theta2'] = 90.000 * (np.pi/180)
exp_val['length_to_lens'] = 71.8
exp_val['radius_of_lens'] = 7.5
exp_val['L']        = 1.42          # Laser beam length (cm) imaged onton fiber
exp_val['gjeven']   = 6
exp_val['gjodd']    = 3

# Transmissions
exp_val['Twin1']    = 0.9
exp_val['Tlens1']   = 0.995
exp_val['Tmirrors1']= 0.997
exp_val['Tfiber']   = 0.587
exp_val['Tspect1']  = 0.72
exp_val['Tcolllens']= 0.849
exp_val['Tfiberimage1'] = 64/75
exp_val['Tpmtlens1'] = 0.849

def collection_optics_solid_angle(length_to_lens, radius_of_lens):
    # The solid angle that is collected by the collection 
    # optics. length_to_lens is the distance from the scattering volume to the
    # location of the collection lens. radius_of_lens is the radius of the 
    # collection lens
    value = 2*np.pi*(1-np.cos(np.arctan(radius_of_lens/length_to_lens)))
    
    return value


def lambda_raman_stokes(l, j):
    B = exp_val['N2_rot_constant']
    value = l + l**2 * (B)*(4*j+6)
    return value


def lambda_thermal(Te):
    l = exp_val['laser_wavelength']
    alpha = exp_val['theta2']
    c1 = 2*l*np.sin(alpha/2)
    c2 = np.sqrt((2*Te)/(511706.544))
    value = c1 * c2
    return value


def laser_photons(E_pulse):
    value = E_pulse * (exp_val['laser_wavelength']/(exp_val['h'] * exp_val['c'])) * 10**-9
    return value


def QEPMTH742240plusH1170640(l):
    # PMT quantum efficiency
    value = -1* (3.0453*10**-4)*l + 0.565053
    return 1


def optical_efficiency(*args):
    value = 1
    for arg in args:
        value = value * arg
        
    return value
    

def coef(E_pulse, n, L, length_to_lens, radius_of_lens, theta):
    # LaserPhotons is the number of photons in a given laser pulse. 
    # (7.9188*10^-26) is the electron radius squared in cm^2. L is the length 
    # of the scattering volume along the laser beam that is being imaged. 
    # ne is the electron density in the scattering volume. 
    # Finally \[Theta] is the angle between the laser polarization and the 
    # collection optics (the Sin (\[Theta])^2 term is the dipole \
    # scattering pattern). 
    c1 = laser_photons(E_pulse)
    c2 = exp_val['electron_radius**2']
    c3 = collection_optics_solid_angle(length_to_lens, radius_of_lens)
    c4 = n / np.sqrt(np.pi) * np.sin(theta)**2
    
    value = c1 *c2 * L * c3 * c4
    
    return value
    
    
def thomson_scattered_photons(E_pulse, n, Te, wavelength):
    c1 = coef(E_pulse, n, exp_val['L'], exp_val['length_to_lens'], 
              exp_val['radius_of_lens'], exp_val['theta1'])

    c2 = lambda_thermal(Te)
    c3 = np.exp(-1*((wavelength - exp_val['laser_wavelength'])**2/(c2**2)))
    
    value = (c1 / c2) * c3

    return value


def thomson_channel_photons(E_pulse, n, Te, min_wavelength, max_wavelength):
    n_steps = 100
    step = (max_wavelength - min_wavelength)/n_steps
    x = np.linspace(min_wavelength, max_wavelength, n_steps)
    y = thomson_scattered_photons(E_pulse, n, Te, x)
    total_int = sum(y) * step
    total = total_int/(max_wavelength - min_wavelength)
    
    return total


def thomson_channel_volts(E_pulse, n, Te, min_wavelength, max_wavelength):
    n_steps = 100
    step = (max_wavelength - min_wavelength)/n_steps
    x = np.linspace(min_wavelength, max_wavelength, n_steps)
    y = thomson_scattered_photons(E_pulse, n, Te, x)
    resistance = 25
    gain = 2 * 10**5
    tau = 20 * 10**-9
    e = 1.60217662 * 10 **-19
    
    
    y = (gain * y * resistance * e)/tau
    
    total_int = sum(y) * step 
    total = total_int/(max_wavelength - min_wavelength)
    
    return total


def raman_coef(E_pulse, n):
    # taking out the TS values for raman scattering coeff and then adding 
    # in the raman specific values. 
    # Note that the density is being converted into cm^-3 from m^-3. Also 
    # the depolarization ratio is included as 3/4 for linear molecules 
    # (all assuming perpendicular scattering geometry)
    c1 = coef(E_pulse, n, exp_val['L'], exp_val['length_to_lens'], 
              exp_val['radius_of_lens'], exp_val['theta1'])
    c2 = np.sqrt(np.pi)/exp_val['electron_radius**2']
    c3 = (64 * np.pi**4)/45
    c4 = .75
    c5 = exp_val['anisotropy']
    
    value = c1 * c2 * c3 * c4 * c5  
    
    return value

def raman_crosssection(l, j):
    c1 = (64 * np.pi**4)/45
    c2 = .75
    c3 = exp_val['anisotropy']
    c4 = (3 * (j + 1) * (j + 2))/(2 * (2 * j + 1)*(2*j+3))
    c5 = (1 / (lambda_raman_stokes(l, j)))**4
    
    value = c1 * c2 * c3 * c4 * c5
    
    return value



def raman_distribution(j, T, gj):
    # j distribution of raman values with T temperature of N2 gas in K and 
    # finally gj is degeneracy for whether j is even or odd
    c1 = gj * ((2 * j) + 1)
    c2 = (2 * exp_val['h'] * exp_val['c'] * exp_val['N2_rot_constant'] * 10**2) / (9 * exp_val['kB'] * T)
    c3 = -(exp_val['h'] * exp_val['c'] * exp_val['N2_rot_constant'] * 10**2 * j * (j+1))/(exp_val['kB']*T)
    c4 = (3 * (j + 1) * (j + 2))/(2 * ((2 * j) + 1)*((2*j)+3))
    
    value = c1 * c2 * np.exp(c3) * c4

    return value


def raman_scattered_photons(E_pulse, n, j, T, gj):
    # rotational stokes raman scattered photonss per unit wavelength
    c1 = raman_coef(E_pulse, n)
    c2 = raman_distribution(j, T, gj)
    c3 = (1/(lambda_raman_stokes(exp_val['laser_wavelength'], j)*10**-7))**4
    
    value = c1 * c2 * c3
    
    return value



def total_photoelectrons_raman_center_function(E_pulse, p, T, 
                                           wavelength_min, wavelength_max):
    c1 = optical_efficiency(exp_val['Twin1'], exp_val['Tlens1'], 
                           exp_val['Tmirrors1'], exp_val['Tfiber'],
                           exp_val['Tspect1'], exp_val['Tcolllens'],
                           exp_val['Tfiberimage1'], exp_val['Tpmtlens1'])

    c1 = 1
    
    n = ((p/(7.5006*10**-3))/(exp_val['kB'] * T))*10**-6
    c2 = 0

    for j in range(0, 60):
        wavelength = lambda_raman_stokes(exp_val['laser_wavelength'], 2 * j)
        if wavelength <= wavelength_max and wavelength >= wavelength_min:
            c2 = c2 + (raman_scattered_photons(E_pulse, n, 2 * j, T, 
                                             exp_val['gjeven']) * 
                       QEPMTH742240plusH1170640(lambda_raman_stokes(exp_val['laser_wavelength'], 2 * j)))

        
    c3 = 0
    for j in range(0, 60):
        wavelength = lambda_raman_stokes(exp_val['laser_wavelength'], 2 * j + 1)
        if wavelength <= wavelength_max and wavelength >= wavelength_min:
            c3 = c3 + (raman_scattered_photons(E_pulse, n, 2 * j + 1, T, 
                                             exp_val['gjodd']) * 
                       QEPMTH742240plusH1170640(lambda_raman_stokes(exp_val['laser_wavelength'], 2 * j + 1)))

            
    value = c1 * (c2 + c3)
    
    return value
        

def step_function_array(start, stop, height):
    frac = (stop - start)/20
    x = np.linspace(start - frac, stop + frac, 110)
    y = np.array([0] * 110)
    y[5:104] = height
    return x, y
    

def plot_thomson_channels(height):
    x1, y1 = step_function_array(533.5, 539, height)
    plt.plot(x1, y1, 'k')
    x1, y1 = step_function_array(539.5, 545, height)
    plt.plot(x1, y1, 'k')  
    x1, y1 = step_function_array(545.5, 551, height)
    plt.plot(x1, y1, 'k')    
    x1, y1 = step_function_array(551.5, 557, height)
    plt.plot(x1, y1, 'k') 
    x1, y1 = step_function_array(557.5, 563, height)
    plt.plot(x1, y1, 'k')
    return
    
#x1 = TotalPhotoelectronsRamanCenterFunction(.8, 50, 295, 545, 551)
x2 = raman_scattered_photons(.8, ((50/(7.5006*10**-3))/(exp_val['kB'] * 295))*10**-6, 35,
                          295, exp_val['gjeven'])




"""
Pressure = np.linspace(0, 50, 100)
Photons = total_photoelectrons_raman_center_function(1.8, Pressure, 295, 536, 561)

a = np.loadtxt('170929_photon_counts_combined_a.txt')
b = np.loadtxt('170929_photon_counts_combined_b_edit.txt')


pressure_a = np.loadtxt('170929_pressure_torr_a.txt')
pressure_b = np.loadtxt('170929_pressure_torr_b_edit.txt')

weights_b = np.loadtxt('weights_b.txt')
weights_a = weights_b[1:len(a)]

plt.figure()





plt.plot(Pressure, Photons, c='k')
plt.scatter(pressure_a, a, c = 'r')
fit1 = np.polyfit(Pressure, Photons, 1)
label1 = str('Theory: y = ' + str(np.round(fit1[0],2)) + 'x')

plt.plot(np.unique(Pressure), np.poly1d(np.polyfit(Pressure, Photons, 1))(np.unique(Pressure)),
         color='k', label=label1)

fit2 = np.polyfit(pressure_a, a, 1)
label2 = str('Data: y = ' + str(np.round(fit2[0],2)) + 'x' )

plt.plot(np.unique(pressure_a), np.poly1d(np.polyfit(pressure_a, a, 1))(np.unique(pressure_a)),
         color='r', label = label2)

plt.xlabel('Pressure (Torr)', fontsize = 15, weight ='bold')
plt.ylabel('Photons', fontsize = 15, weight ='bold')
title = str("Predicted Raman Scattering \n (536 nm - 561 nm)")
plt.title(title, fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')
plt.legend()
plt.savefig('test_1_theory_vs_data.png', format='png', dpi = 1000)
plt.show()

"""
"""

Pressure = np.linspace(0, 50, 100)
Photons = total_photoelectrons_raman_center_function(1.8, Pressure, 295, 543, 565)

b = np.loadtxt('170929_photon_counts_combined_b_edit.txt')

pressure_b = np.loadtxt('170929_pressure_torr_b_edit.txt')

weights_b = np.loadtxt('weights_b.txt')
weights_b = weights_b[1:len(b)]

plt.figure()



plt.plot(Pressure, Photons, c='k')
plt.scatter(pressure_b, b, c = 'b')
fit1 = np.polyfit(Pressure, Photons, 1)
label1 = str('Theory: y = ' + str(np.round(fit1[0],2)) + 'x')

plt.plot(np.unique(Pressure), np.poly1d(np.polyfit(Pressure, Photons, 1))(np.unique(Pressure)),
         color='k', label=label1)

fit2 = np.polyfit(pressure_b, b, 1)
label2 = str('Data: y = ' + str(np.round(fit2[0],2)) + 'x' )

plt.plot(np.unique(pressure_a), np.poly1d(np.polyfit(pressure_a, a, 1))(np.unique(pressure_a)),
         color='b', label = label2)

plt.xlabel('Pressure (Torr)', fontsize = 15, weight ='bold')
plt.ylabel('Photons', fontsize = 15, weight ='bold')
title = str("Raman Scattering \n(543 nm - 565 nm)")
plt.title(title, fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')
plt.legend()
#plt.savefig('test_2_theory_vs_data.png', format='png', dpi = 1000)
plt.show()
"""
"""
plt.figure()
x = np.linspace(532, 563, 200)
y = thomson_scattered_photons(1.69, 1*10**13, 100, x)
plt.plot(x, y,'r', label = 'Te: 100 eV')
y = thomson_scattered_photons(1.69, 1*10**13, 150, x)
plt.plot(x, y, 'b', label = 'Te: 150 eV')
y = thomson_scattered_photons(1.69, 1*10**13, 200, x)
plt.plot(x, y, 'k', label = 'Te: 200 eV')
print(max(y)/10)
plot_thomson_channels(max(y)/5)

plt.xlabel('Wavelength (nm)', fontsize = 15, weight ='bold')
plt.ylabel('Photons', fontsize = 15, weight ='bold')
plt.title('Estimated Thomson Scattered Photons', fontsize = 15, weight ='bold')
plt.legend(fontsize = 12,loc='upper right')
plt.show()

plt.figure()
x = np.linspace(532, 563, 200)
y = thomson_scattered_photons(1.69, 1*10**13, 100, x)
plt.plot(x, y,'r', label = 'Total Scattered')

c1 = optical_efficiency(exp_val['Twin1'], exp_val['Tlens1'], 
                       exp_val['Tmirrors1'], exp_val['Tfiber'],
                       exp_val['Tspect1'], exp_val['Tcolllens'],
                       exp_val['Tfiberimage1'], exp_val['Tpmtlens1'])
y = y * c1 
plt.plot(x, y, 'b', label = 'Collected by PMT')

plt.xlabel('Wavelength (nm)', fontsize = 15, weight ='bold')
plt.ylabel('Photons', fontsize = 15, weight ='bold')
plt.title('Estimated Thomson Scattered Photons \n 100 eV Plasma', fontsize = 15, weight ='bold')
plt.legend(fontsize = 12,loc='upper right')
plt.show()



"""
"""
x = np.linspace(1, 300, 100)

y1 = thomson_channel_photons(1.69, 1*10**13, x, 533.5, 539 )[1]
y2 = thomson_channel_photons(1.69, 1*10**13, x, 539.5, 545 )[1]
y3 = thomson_channel_photons(1.69, 1*10**13, x, 545.5, 551 )[1]
y4 = thomson_channel_photons(1.69, 1*10**13, x, 551.5, 557 )[1]
y5 = thomson_channel_photons(1.69, 1*10**13, x, 557.5, 563 )[1]

plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)
plt.plot(x, y4)
plt.plot(x, y5)

print(thomson_channel_photons(1.69, 1*10**13, 100, 532, 532.5))
print(thomson_channel_volts(1.69, 1*10**13, 100, 532, 532.5))
"""


