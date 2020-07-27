
import matplotlib.pyplot as plt
import MDSplus as mds
import numpy as np
from scipy import signal

#import peakutils

from lmfit.models import GaussianModel, ConstantModel


class Thomson:
    
    def __init__(self, shot):
        self.shot = shot
        
        
        def get_raw_data(shot):
            tree = 't' + str(shot)[0:6]
            
            #conn = mds.connection.Connection('mds.physics.auburn.edu')
            conn = mds.connection.Connection('131.204.212.37')
            conn.openTree(tree, shot)
            
            pmt_data        = -1*conn.get('thomson:ch1').data()  
            diode_data      =  1*conn.get('thomson:ch2').data()
            ch3_data        =  1*conn.get('thomson:ch3').data()
            ch4_data        = -1*conn.get('thomson:ch4').data()
        
            timebase        = conn.get('thomson:data_dt').data()
            t0 = conn.get('parameters:timing:trig_3c_dly').data()
            
            conn.closeAllTrees()
    
            length          = len(pmt_data)
            time            = np.linspace(t0, t0 + timebase*length, length)
            #time            = np.linspace(0, 200, length)
            
            return  time, pmt_data, ch3_data, diode_data, ch4_data


        [self.time, self.pmt_data, self.ch23data, self.diode_data, 
         self.ch4_data] = get_raw_data(self.shot)
        
        
    def total_photons(self, pmt_gain, pmt_quantum_efficiency, 
                      scope_resistance):
        e  = 1.60217662 * 10 **-19
        mu = pmt_gain
        QE = pmt_quantum_efficiency
        R  = scope_resistance
        
        # Total photons hitting the PMT cathode     
        time, data = self.get_pmt_current_data_smooth(R)
        
        # Put time in nanoseconds and remove offset
        time = (time - 1600) * 10**9

        # Fit the current profile
        fit = OneGaussianFit(time, data, print_report = False)
        
        fit.x           = (fit.x * 10**-9) + 1600
        
        # Get the total charge collected (Amps x Nanoseconds)
        total_charge = fit.integrate_gaussian() 
        
        # Total charge in Coulombs
        total_charge = total_charge * 10.**-9
        
        anode_electron_count = total_charge / e

        cathode_electron_count = anode_electron_count / mu
        
        # Photons hitting cathode
        photon_count = cathode_electron_count / QE
        
        return photon_count[0], photon_count[1], fit.x, fit.y_fit, fit.y_fit_ini
    
    
    def volts_to_current(self, voltage, resistance):
        # Takes the raw voltage and returns the number of electrons per second
        j = voltage/resistance
        
        return j
        
       
    def get_pmt_current_data(self, resistance, gain, pulse_length):
        time = self.time
        R = resistance
        
        corrected_pmt_data = self.pmt_data/R  
        return  time, corrected_pmt_data           


    def get_pmt_current_data_smooth(self, resistance):
        # Current
        R = resistance
        
        time, smooth_data = self.get_pmt_data_smooth2() 
        
        corrected_pmt_data = self.volts_to_current(smooth_data, R)    
        return  time, corrected_pmt_data


    def get_pmt_data_smooth1(self):
        time, data = self.time, self.pmt_data
        #time, data = self.get_corrected_pmt_data()
        
        smooth_data = signal.savgol_filter(data, 9001, 2)
        return time, smooth_data
    
    
    def get_pmt_data_smooth2(self):
        time, data = self.get_pmt_data_smooth1()    
        smooth_data2 = signal.savgol_filter(data, 8001, 2)
        return time, smooth_data2
     
    
    def get_corrected_pmt_data_smooth2(self):
        time, data = self.get_pmt_data_smooth2()
        R = 1
        mu = 2 * 10**5
        tau = 2 * 10**-9
        corrected_data = self.raw_volt_to_n(data, R, tau, mu)
        return time, corrected_data
    
    
    def get_diode_data_smooth(self):
        time, data = self.time, self.diode_data
        smooth_data = signal.savgol_filter(data, 4001, 1)
        return time, smooth_data



class OneGaussianFit():
    
    def __init__(self, x, y, print_report):
        self.x                  = x
        self.y                  = y
        self.y_ini              = 0
        self.index_ini          = 0
        self.print_report_val   = print_report
        self.y_fit, self.y_fit_ini, self.plsq, self.plsq_err = self.one_gaussian_fit() 

        
    def find_peaks(self):
        x               = self.x
        y               = self.y
        #index           = peakutils.indexes(y)
        #print(index)
        index           = [np.argmax(y)]
        #print(index)
        return x, y, index    


    def one_gaussian_fit(self):
        x, y, index = self.find_peaks()
        
        def find_nearest(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()

            return idx
        
        # Starting Values
        ini_center = x[index[0]]
        ini_scale  = y[index[0]] - y[100]

        half_scale = ini_scale/2.

        first = find_nearest(y, half_scale)
        half_width = abs(ini_center - x[first])
        ini_stand_dev = (half_width * 1) / 2.355
        ini_offset = y[100]
        ini_scale = ini_scale * np.sqrt(np.pi * 2) * ini_stand_dev

        #lmfit GaussianModel
        model = GaussianModel(prefix='peak_') + ConstantModel()
        params = model.make_params(c=ini_offset, peak_center=ini_center, 
                                   peak_sigma=ini_stand_dev, 
                                   peak_amplitude=ini_scale)
        
        result = model.fit(y, params, x=x)
        
        if self.print_report_val:
            print(result.fit_report())
        
        offset          = result.params['c'].value
        center          = result.params['peak_center'].value
        scale           = result.params['peak_amplitude'].value
        stand_dev       = result.params['peak_sigma'].value
        
        offset_err      = result.params['c'].stderr
        center_err      = result.params['peak_center'].stderr
        scale_err       = result.params['peak_amplitude'].stderr
        stand_dev_err   = result.params['peak_sigma'].stderr
        
        plsq        = [offset, center, stand_dev, scale]
        plsq_err    = [offset_err, center_err, stand_dev_err, scale_err]
        
        return result.best_fit, result.init_fit, plsq, plsq_err
    
    
    def integrate_gaussian(self):
        #plsq        = self.plsq
        #plsq_err    = self.plsq_err
        
        #int2 = (plsq[0][1] * plsq[0][2]) * np.sqrt(np.pi * 2)
        #integral = plsq[3] * plsq[2] * np.sqrt(np.pi * 2)
        integral = self.plsq[3]
        #err = integral * np.sqrt((plsq_err[3]/plsq[3])**2 + (plsq_err[2]/plsq[2])**2)
        err = self.plsq_err[3]
        
        return np.array([integral, err])      
                

"""
plt.figure()
s1 = Thomson(17092920)

time1, data1 = s1.time, s1.pmt_data
time2, data2 = s1.get_pmt_current_data_smooth(25)


print('Photon Count')
mu = 2 * 10**5
photons, err, x, y, y_ini = s1.total_photons(mu, .4, 25)
print(photons)
print(err)



plt.xlabel('Time (s)', fontsize = 15, weight ='bold')
plt.ylabel('Current (A)', fontsize = 15, weight ='bold')
plt.title('PMT Data \n Shot: 17092920', fontsize = 15, weight ='bold')
plt.xticks(fontsize = 13, weight = 'bold')
plt.yticks(fontsize = 13, weight = 'bold')

plt.plot(time2, data2, 'k', label = 'Smoothed PMT Current')
plt.plot(x, y, 'r', label = 'Gaussian Fit')
plt.legend(loc = 1)
#plt.plot(x, y_ini, 'y')

plt.savefig('17092920_smooth_current_test.png', format='png', dpi = 1000,  bbox_inches='tight')

"""






