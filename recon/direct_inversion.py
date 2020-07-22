# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 20:20:00 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import numpy as np
import numpy.ma as ma
from flux_surface_grid_inv_direct import FluxSurfaceGrid
#from function_recon import function0, function1, function2, function3
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from scipy.signal import savgol_filter
import time
import matplotlib.ticker as mticker
from matplotlib.offsetbox import AnchoredText

f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
c = lambda x : r'${}$'.format(f._formatSciNotation('%1.1e' % x))
t1 = time.time() 
#print("Took " + str(round(time.time() - t1, 4)) + ' sec: Import Time' )



flatten = np.ndarray.flatten
matmul = np.matmul
pinv = np.linalg.pinv

class ConstrainedTransform:
    
    def __init__(self, 
                 wout_filepath = None,  
                 dropout=True,
                 grid_size = 31,
                 camera_points_filepath=None,
                 lcf_confined=True):
        
        self.data = {}
        self.data['wout_filepath'] = wout_filepath
        self.data['dropout'] = dropout
        
        self.data['grid_size'] = grid_size
        self.data['camera filepath'] = camera_points_filepath
        self.lcf_confined=lcf_confined
        
        
    def setup_recon(self):
        t0 = time.time()
        self.initialize_grid(self.data['wout_filepath'])
        
        print('Grid Initialized:',str(round(time.time() - t0, 4)),'s')
        
        self.data['xdata'] = np.linspace(0, self.n_cam-1, self.n_cam)
        
        return
    

        
    def initialize_grid(self, wout_filepath):
        self.grid = FluxSurfaceGrid(wout_filepath, size=self.data['grid_size'])        
        self.grid.make_grid()
        
        f_zero = np.ones(self.grid.s_grid.shape)
        self.grid.update_grid_from_array(f_zero)
        self.zero_grid = self.grid.grid['grid_data']
        
        
        O,D = self.load_camera_points(self.data['camera filepath'])
        self.T = self.grid.get_multiple_chord_pathlengths(O,D)

        return


    def init_inversion(self):
        raw_data = self.data['raw data']
        self.T_fl =[]
        for arr in self.T:
            self.T_fl.append(flatten(arr))
        
        self.T_fl = np.array(self.T_fl)
        
        self.init_grid      = matmul(pinv(self.T_fl), raw_data).reshape((self.data['grid_size'],self.data['grid_size']))
        self.init_grid_fl   = flatten(self.init_grid)
        
        
        self.H0 = matmul(self.init_grid_fl.T, self.init_grid_fl)
        
        #print(self.init_grid.shape)
        g1 = np.gradient(self.init_grid)#/ self.grid.grid['x_step']
        
        #print(g1.shape)        
        x1 = flatten(g1[1])
        y1 = flatten(g1[0])
        
        self.H1 = matmul(x1.T, x1) + matmul(y1.T, y1)
        
        x2 = flatten(np.gradient(g1[1])[1])#/self.grid.grid['x_step'])
        y2 = flatten(np.gradient(g1[0])[0])#/self.grid.grid['y_step'])
        
        self.H2 = matmul(x2.T, x2) + matmul(y2.T, y2)
        
        
        sm_win = self.data['grid_size']//7
        sm_win_s = len(self.grid.s)//3
        sm_win_theta = self.grid.n_theta//7
        
        
        order = 3
        s_order = 3
        theta_order = 3
        
        if sm_win % 2==0:
            sm_win += 1
        if order >= sm_win:
            order = sm_win-1
            
        if sm_win_s % 2==0:
            sm_win_s += 1
        if s_order >= sm_win_s:
            s_order = sm_win_s-1
            
        if sm_win_theta % 2==0:
            sm_win_theta += 1
        if theta_order >= sm_win_theta:
            theta_order = sm_win_theta-1            
            
            
        #print('s ',sm_win_s, s_order)    
        self.grid.grid['grid_data'] = self.init_grid
        self.grid.get_s_theta_points()
        
        sm1_s = savgol_filter(self.grid.s_theta_array, sm_win_s, s_order, axis=0)
        sm1_theta = savgol_filter(self.grid.s_theta_array, sm_win_theta, theta_order, axis=1)

        
        sm1_x = savgol_filter(self.init_grid, sm_win, order, axis=1)
        sm1_y = savgol_filter(self.init_grid, sm_win, order, axis=0)
        
        #plt.figure()
        #plt.plot(self.init_grid[0], 'k')
        #plt.plot(sm1_x[0]-1)        
        
        sm1 = (sm1_x + sm1_y) * .5
        sm1 = sm1_x
        #plt.figure()
        #plt.imshow(self.grid.s_theta_array)
        
        #plt.figure()
        #plt.imshow(sm1_theta)

        #plt.figure()
        #plt.imshow(sm1_s)        
        sm1_sth = (sm1_theta + sm1_s) *.5
        sm1_sth = sm1_s
        sm1_sth_pass = sm1_sth
        self.grid.update_grid_from_s_theta_array(sm1_sth)
        sm1_sth = self.grid.grid['grid_data']
        
        
        sm2_x = savgol_filter(sm1, sm_win, order, axis=1)
        
        sm2_y = savgol_filter(sm1, sm_win, order, axis=0)
        
        
        sm2_s = savgol_filter(sm1_sth_pass, sm_win_s, s_order, axis=0)
        sm2_theta = savgol_filter(sm1_sth_pass, sm_win_theta, theta_order, axis=1)
        
        sm2 = (sm2_x + sm2_y) * .5
        sm2 = sm2_x
        
        #plt.figure()
        #plt.imshow(sm2_theta)

        #plt.figure()
        #plt.imshow(sm2_s)         
       
        sm2_sth = (sm2_theta + sm2_s) *.5
        sm2_sth = sm2_s
        self.grid.update_grid_from_s_theta_array(sm2_sth)
        sm2_sth = self.grid.grid['grid_data']
        
        self.SM1 = sm1#_sth#sm1
        self.SM2 = sm2#_sth#sm2
        
        
        
        self.a = matmul(self.T_fl.T, self.T_fl)
        
        #self.data['starting parameters'] = [5E-10, 1E-6, 1E-4]
        
        return
        

        
        
    def run_recon(self, raw_data=None, raw_data_sigma=None,
                  mask=None,
                  wrapper = 1,
                  fixed_values=0):

        self.mask = mask
        #self.make_bounds()
        
        t0 = time.time()
        print('\n')
        print('Reconstruction Started')        
        self.data['raw data'] = raw_data
        self.data['raw data sigma'] = raw_data_sigma

        self.init_inversion()
        
        print()
        print('First Run Started')                
        t1 = time.time() 
        
        
        if wrapper == 1:
            wrap_fun = self.signal_wrapper1
            init_val = list([0, -5, 10])
            bnds = [(0,100), (-15,100), (-15,100)]
        elif wrapper == 2:
            wrap_fun = self.signal_wrapper2
            init_val = list([.1, .1, .9])
            bnds = [(-10,10), (-10,10), (-10, 10)]
            
            if self.lcf_confined:
                self.grid.grid['grid_data'] = (init_val[0]*self.init_grid+init_val[1]*self.SM1+init_val[2]*self.SM2)*self.zero_grid
            else:
                self.grid.grid['grid_data'] = (init_val[0]*self.init_grid+init_val[1]*self.SM1+init_val[2]*self.SM2)
        
            self.base_sig = self.grid.evaluate_signals(self.T)
            r = abs(self.data['raw data'][mask] - self.base_sig[mask])/self.data['raw data sigma'][mask]
            self.base_chisquared = sum(r[0]*r[0])
            
            #print(self.base_chisquared)
            sm_x = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=1), axis=1))))
            sm_y = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=0), axis=0))))
 
            self.base_smoothness = sm_x + sm_y        
                       
            
        else:
            print('Invalid Wrapper Number:', wrapper)
            return

        
        result = minimize(wrap_fun, init_val, bounds=bnds)#,method='L-BFGS-B')
        
        
        print('First Run Completed ',str(round(time.time() - t1, 4)),'s')

            
        
        print(result)
        #self.data['final parameters'] = solution
        #self.data['covariance'] = covariance
        #self.perr = np.sqrt(np.diag(self.data['covariance']))
        
        
        #recon_signals = self.grid.evaluate_signals(self.camera_array)
        
        self.data['reconstructed signals'] = self.grid.evaluate_signals(self.T)

        
        #self.sigma_sig = wrapper2(self.data['xdata'], self.perr)
        #self.grid.plot_grid()
        
        
    
        self.data['Duration'] = str(round(time.time() - t0, 4))
        
        
    def signal_wrapper1(self, *param):
        parameters = [p for p in param][0]
        mask=self.mask
        
        l0 = 0#1*10**parameters[0]
        l1 = 0#1*10**parameters[1]
        l2 = parameters[2]
    
        
        self.b = (self.a + l0*self.H0 + l1*self.H1 + l2*self.H2)
        self.b_inv = pinv(self.b)
        
        #print('T shape',self.T.shape)
        
        self.grid.grid['grid_data'] = abs(matmul(self.b_inv, matmul(self.T_fl.T,self.data['raw data'])))
        self.grid.grid['grid_data'] = self.grid.grid['grid_data'].reshape((self.data['grid_size'], self.data['grid_size']))
        
        if self.lcf_confined:
            self.grid.grid['grid_data'] = self.grid.grid['grid_data']*self.zero_grid
        else:
            self.grid.grid['grid_data'] = self.grid.grid['grid_data']

        
        
        signals = self.grid.evaluate_signals(self.T)
        
        
        dof = self.n_cam 
        r = abs(self.data['raw data'][mask] - signals[mask])/self.data['raw data sigma']#[mask]

        chisquared = sum(r[0]*r[0])

        reduced_chisquared = chisquared/dof
        
        self.data['Chi^2'] = chisquared
        self.data['Chi^2 reduced'] = reduced_chisquared        
        
        
        sm_x = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=1), axis=1))))
        sm_y = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=0), axis=0))))
        
        smoothness = sm_x + sm_y
        #min_factor =.5* self.data['Chi^2'] + smoothness
        min_factor = (self.data['Chi^2']/self.base_chisquared) + (smoothness/self.base_smoothness)
        #print(min_factor)
        return min_factor


    def signal_wrapper2(self, *param):
        mask = self.mask
        parameters = [p for p in param][0]
        
        l0 = parameters[0]
        l1 = parameters[1]
        l2 = parameters[2]

        #self.grid.grid['grid_data'] = (l0*self.init_grid + l1*self.SM1 + l2*self.SM2)
        #self.grid.grid['grid_data'] = self.init_grid
        #base_sig = self.grid.evaluate_signals(self.T)
        #dof = self.n_cam 
        #r = abs(self.data['raw data'][mask] - base_sig[mask])/self.data['raw data sigma'][mask]
        #base_chisquared = sum(r[0]*r[0])
        #sm_x = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=1), axis=1))))
        #sm_y = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=0), axis=0))))
 
        #base_smoothness = sm_x + sm_y        
        
        new_grid = (l0*self.init_grid + l1*self.SM1 + l2*self.SM2)
        
        #new_grid = self.SM2
        if self.lcf_confined:
            self.grid.grid['grid_data'] = new_grid*self.zero_grid
        else:
            self.grid.grid['grid_data'] = new_grid
            
        
        signals = self.grid.evaluate_signals(self.T)
    
        dof = self.n_cam 
        r = abs(self.data['raw data'][mask] - signals[mask])/self.data['raw data sigma'][mask]
        chisquared = sum(r[0]*r[0])
        reduced_chisquared = chisquared/dof
        
        self.data['Chi^2'] = chisquared
        self.data['Chi^2 reduced'] = reduced_chisquared    
        
        
        sm_x = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=1), axis=1))))
        sm_y = sum(sum(abs(np.gradient(np.gradient(self.grid.grid['grid_data'], axis=0), axis=0))))
 
        smoothness = sm_x + sm_y
        
        
        min_factor = (self.data['Chi^2']/self.base_chisquared) + (smoothness/self.base_smoothness)
        #min_factor = smoothness
        #print(min_factor)
        #print(self.data['Chi^2']/self.base_chisquared)
        #print(min_factor)
        return min_factor
                    
        
    
    def load_camera_points(self, camera_path):
        
        points = np.load(camera_path)
        O, D = [],[]

        for ii in range(0,len(points)):
            p1 = points[ii][0]
            p2 = points[ii][1]
            
            O.append(p1)
            d = np.array(p2) - np.array(p1)
            d = d/np.linalg.norm(d)
            
            D.append(d.tolist())
            
        self.n_cam = len(D)            
        return O, D
                    
        
        
    def print_recon_results(self):
        print()
        print('Reconstruction Completed')
    
        print('Time Elapsed:',self.data['Duration'],'s')
        print('Chi^2 :',"{:.2E}".format(self.data['Chi^2']))
        print('Reduced Chi^2 :', "{:.2E}".format(self.data['Chi^2 reduced']))
        print('Residuals^2 :',"{:.2E}".format(self.data['Residuals squared']))        

        print('Number of Initial Parameters:',str(len(self.data['final parameters'])))            
        #print('Number of Final Parameters:',str(fitting_parameters))
        print('Number of Signals:',str(self.n_cam))
        print()
        #print('Final Parameters: ')
        #print_param = self.data['final parameters'].reshape(int(len(solution)/2),2)
        
        return
    
    
    
    
    
    def plot_results(self):
        plt.figure()
        plt.plot(self.data['xdata'], self.data['raw data'],'k', label='Raw Data')

        plt.fill_between(self.data['xdata'],
                         self.data['raw data']-self.data['raw data sigma'],
                         self.data['raw data']+self.data['raw data sigma'],
                         color='gray', alpha=.4)#, label = 'Uncertainty')
        plt.plot(self.data['xdata'], self.data['reconstructed signals'], 'r', label='Recon Data')
        
        plt.axvline(x=0, c='b')
        plt.axvline(x=19.2, c='b')
        plt.axvline(x=39.2, c='b')
        plt.axvline(x=18.8, c='r')
        plt.axvline(x=38.8, c='r')
        plt.axvline(x=58.8, c='r')     
        
        """
        plt.fill_between(self.data['xdata'],
                         self.data['reconstructed signals']-self.sigma_sig,
                         self.data['reconstructed signals']+self.sigma_sig,
                         color='r', alpha=.3)#, label = 'Recon Uncertainty')        
        """
        legend_properties = {'weight':'bold',
                             'size' : 13}
        plt.legend(loc=0, prop=legend_properties)
        title = str('Raw vs. Reconstructed Data \n' +
                    r'$SS_{res}$ = ' + str(round(self.data['Residuals squared'],2)) + '  '
                    r'$\chi ^2$ = ' + str(round(self.data['Chi^2'],2)) + '  '
                    r'$\chi_R ^2$ = ' + str(round(self.data['Chi^2 reduced'],2)))
        plt.title(title,fontsize = 15, weight ='bold')
        plt.xlabel('Channel Number',fontsize = 15, weight ='bold')
        plt.ylabel('Relative Intensity',fontsize = 15, weight ='bold')
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')
        plt.ylim([max(self.data['raw data'])*-.5, max(self.data['raw data'])*2])

        


    def load_cameras_files(self, paths):
        master = []
        
        for path in paths:
            master+=np.load(path).tolist()
            
        return master



