# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 09:39:49 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""

from vmec import wout_file
from pathlength import Pathlength2D
from flux_surface_inversion import InvertChords
from flux_surface_grid_inv_direct import FluxSurfaceGrid
from direct_inversion import ConstrainedTransform
#from cthdata import CTHData, find_closest_index
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from cthdata import find_closest_index
from scipy.signal import savgol_filter
import matplotlib
matplotlib.use('Agg')
def gaussian(x, mu, sigma):
    #A = 1/(sigma * np.sqrt(2*np.pi))
    B = -.5*((x-mu)/sigma)**2
    
    y = np.exp(B)
    return y


def make_noisy(array, noise_percent):
    hn = array*(1+noise_percent)
    ln = array*(1-noise_percent)


    new_array = np.random.uniform(ln, hn)
    return new_array




class CTHBolometerInversion:
    
    def __init__(self,
                 wout_filepath = None,
                 camera_points_filepath=None,
                 lcf_confined=True):

        self.data = {}
        self.data['wout_filepath'] = wout_filepath
        self.data['camera_filepath'] = camera_points_filepath
        self.data['points'] = np.load(camera_points_filepath)
        self.data['fine_grid_size'] = 310
        self.data['coarse_grid_size'] = 31
        self.data['camera_toroidal_angle'] = 252
        self.make_grids()
        self.get_chord_matrices()
        self.fs_plot = 0
        self.svd_plot = 0
        self.residuals_plot = 0
        self.count = 1
        self.lcf_confined = lcf_confined
        
        
        

    def flux_surface_fit(self, signals, sigma, estimate_uncertainty=False):
        self.signals = signals
        self.sigma = sigma
        self.fs_plot = 1
        self.flux_surface_inversion(signals, sigma, estimate_uncertainty=estimate_uncertainty)
        
        """
        self.inv_flux[-1] = (self.inv_flux[-1] + self.inv_flux[-2])/2
        
        fsf_order = 1
        fsf_win = len(self.inv_flux)//3
        
        if fsf_win % 2==0:
            fsf_win += 1
        if fsf_order >= fsf_win:
            fsf_order = fsf_win-1        

        
        
        sm_inv_flux = savgol_filter(self.inv_flux,fsf_win, fsf_order)
        sm_inv_flux2 = savgol_filter(sm_inv_flux,fsf_win, fsf_order)        
        plt.figure()
        plt.plot(self.inv_flux)
        plt.plot(sm_inv_flux)
        plt.plot(sm_inv_flux2)

        self.inv_flux = sm_inv_flux2
        """
        
        
        
        self.fine_grid.update_grid_from_flux_array(self.inv_flux, self.inv_s)
        self.fs_fitted_signal = self.fine_grid.evaluate_signals(self.T_fine)

        
        r = ((signals - self.fs_fitted_signal)/sigma)
        self.fs_chi2 = round(sum(r*r),2)
        
        
        
        if estimate_uncertainty:
            self.fs_plot = 2
            self.fine_grid.update_grid_from_flux_array(self.inv_flux_sigma_u, self.inv_s)
            self.fs_fitted_signal_u = self.fine_grid.evaluate_signals(self.T_fine)
        
            self.fine_grid.update_grid_from_flux_array(self.inv_flux_sigma_d, self.inv_s)
            self.fs_fitted_signal_d = self.fine_grid.evaluate_signals(self.T_fine)        

        return
    
    
    def svd_fit(self, signals, sigma, estimate_uncertainty=False):
        self.signals = signals
        self.sigma = sigma
        self.svd_plot = 1
        self.svd_direct_inversion(signals, sigma, estimate_uncertainty=estimate_uncertainty)
        
        self.coarse_grid.grid['grid_data'] = self.svd_transform.grid.grid['grid_data']
        self.svd_fitted_signal = self.svd_transform.grid.evaluate_signals(self.T_coarse)
        
        r = ((signals - self.svd_fitted_signal)/sigma)
        self.svd_chi2 = round(sum(r*r),2)
        
        if estimate_uncertainty:
            self.svd_plot = 2
            self.svd_fitted_signal_u = self.svd_transform_sigma_u.grid.evaluate_signals(self.T_coarse)
            self.svd_fitted_signal_d = self.svd_transform_sigma_d.grid.evaluate_signals(self.T_coarse)
        
        return
    
    
    def residuals_fit(self, residuals, sigma, estimate_uncertainty=False):
        self.residuals = residuals
        self.sigma = sigma
        self.residuals_plot = 1
        self.residuals_inversion(residuals, sigma, estimate_uncertainty=estimate_uncertainty)
        
        self.coarse_grid.grid['grid_data'] = self.svd_transform_residuals.grid.grid['grid_data']
        self.residuals_fitted_signal = self.svd_transform_residuals.grid.evaluate_signals(self.T_coarse)
        
        r = ((residuals - self.residuals_fitted_signal)/sigma)
        self.residuals_chi2 = round(sum(r*r),2)

        self.combined_residuals = self.fs_fitted_signal + self.residuals_fitted_signal
        r = ((self.signals - self.combined_residuals)/sigma)
        self.combined_signals_chi2 = round(sum(r*r),2)


        if estimate_uncertainty:
            self.residuals_plot = 2
            self.residuals_fitted_signal_u = self.svd_transform_residuals_u.grid.evaluate_signals(self.T_coarse)
            self.residuals_fitted_signal_d = self.svd_transform_residuals_d.grid.evaluate_signals(self.T_coarse)
        
        return
    
    
    def make_grids(self):
        # Make initial grids on which the inversion will be estimated
        # the size for the fine grid is subject to variation
        # the coarse grid size tends to work best when 31x31
        
        
        self.fine_grid = FluxSurfaceGrid(self.data['wout_filepath'], size=self.data['fine_grid_size'])
        self.fine_grid.make_grid()
        self.coarse_grid=FluxSurfaceGrid(self.data['wout_filepath'], size=self.data['coarse_grid_size'])
        self.coarse_grid.make_grid()
        self.combined_grid=FluxSurfaceGrid(self.data['wout_filepath'], size=self.data['coarse_grid_size'])
        self.combined_grid.make_grid()
        self.sim_plot = None
        return        
    
    
    def make_sim_grid(self):
        # make simulation grids for testing
        self.fine_grid_sim = FluxSurfaceGrid(self.data['wout_filepath'], size=self.data['fine_grid_size'])
        self.fine_grid_sim.make_grid()
        self.coarse_grid_sim=FluxSurfaceGrid(self.data['wout_filepath'], size=self.data['coarse_grid_size'])
        self.coarse_grid_sim.make_grid()        
        
        f0_fine = gaussian(self.fine_grid_sim.s_grid, .25, .4)
        f1_fine = self.fine_grid_sim.local_gaussian_polar2(1, .5, .3, 1*np.pi/2, self.fine_grid_sim.s, self.fine_grid_sim.theta)
        f2_fine = self.fine_grid_sim.local_gaussian_polar2(1, .5, .3, 3*np.pi/2, self.fine_grid_sim.s, self.fine_grid_sim.theta)
        fm_fine = make_noisy(f0_fine + f1_fine+0*f2_fine, 0.05)
        
        f0_coarse = gaussian(self.coarse_grid_sim.s_grid, .25, .4)
        f1_coarse = self.coarse_grid_sim.local_gaussian_polar2(1, .5, .3, 1*np.pi/2, self.coarse_grid_sim.s, self.coarse_grid_sim.theta)
        fm_coarse = make_noisy(f0_coarse + f1_coarse, 0.05)        
        
        self.fine_grid_sim.update_grid_from_array(fm_fine)
        self.coarse_grid_sim.update_grid_from_array(fm_coarse)
        return
        
        
    def get_chord_matrices(self):
        self.T_fine   = self.fine_grid.get_mulitple_chord_pathlengths_points(self.data['points'])
        self.T_coarse = self.coarse_grid.get_mulitple_chord_pathlengths_points(self.data['points'])
        return
    
    
    def get_sim_data(self):
        self.make_sim_grid()
        self.sim_plot=True
        
        self.f_fine = self.fine_grid_sim.evaluate_signals(self.T_fine)
        self.f_fine_sigma = self.f_fine*.05 + max(np.ndarray.flatten(self.f_fine)) * .001
        
        self.f_coarse = self.coarse_grid_sim.evaluate_signals(self.T_coarse)
        self.f_coarse_sigma = self.f_coarse*.05 + max(np.ndarray.flatten(self.f_coarse)) * .001        
        return
    
    
    def flux_surface_inversion(self, signals, sigma, estimate_uncertainty=False):
        self.inv = InvertChords(self.data['wout_filepath'],self.data['camera_toroidal_angle'],self.data['points'],
                                signals)
        self.inv_flux = self.inv.inv_values
        self.inv_s = self.inv.s
        
        if estimate_uncertainty:
            self.inv_flux_sigma_u = InvertChords(self.data['wout_filepath'],self.data['camera_toroidal_angle'],self.data['points'],
                                                 signals + sigma).inv_values
            self.inv_flux_sigma_d = InvertChords(self.data['wout_filepath'],self.data['camera_toroidal_angle'],self.data['points'],
                                                 signals - sigma).inv_values 
        
        return 
    
    
    def svd_direct_inversion(self, signals, sigma, estimate_uncertainty=False):
        self.svd_transform = ConstrainedTransform(wout_filepath = self.data['wout_filepath'],
                                                  grid_size=self.data['coarse_grid_size'],
                                                  camera_points_filepath=self.data['camera_filepath'],
                                                  lcf_confined=self.lcf_confined)
            
        self.svd_transform.setup_recon()
        self.svd_transform.run_recon(raw_data = signals, raw_data_sigma=sigma, wrapper=2)
        
        if estimate_uncertainty:
            self.svd_transform_sigma_u = ConstrainedTransform(wout_filepath = self.data['wout_filepath'],
                                                              grid_size=self.data['coarse_grid_size'],
                                                              camera_points_filepath=self.data['camera_filepath'],
                                                              lcf_confined=self.lcf_confined)
        
            self.svd_transform_sigma_u.setup_recon()
            self.svd_transform_sigma_u.run_recon(raw_data = signals+sigma, raw_data_sigma=sigma, wrapper=2)   
            
            self.svd_transform_sigma_d = ConstrainedTransform(wout_filepath = self.data['wout_filepath'],
                                                              grid_size=self.data['coarse_grid_size'],
                                                              camera_points_filepath=self.data['camera_filepath'],
                                                              lcf_confined=self.lcf_confined)
            
            self.svd_transform_sigma_d.setup_recon()
            self.svd_transform_sigma_d.run_recon(raw_data = signals-sigma, raw_data_sigma=sigma, wrapper=2)        

        return        
        
    
    def residuals_inversion(self, residuals, sigma, estimate_uncertainty=False):
        self.svd_transform_residuals = ConstrainedTransform(wout_filepath = self.data['wout_filepath'],
                                                  grid_size=self.data['coarse_grid_size'],
                                                  camera_points_filepath=self.data['camera_filepath'],
                                                  lcf_confined=self.lcf_confined)
            
        self.svd_transform_residuals.setup_recon()
        self.svd_transform_residuals.run_recon(raw_data = residuals, raw_data_sigma=sigma, wrapper=2)
        
        if estimate_uncertainty:
            self.svd_transform_residuals_u = ConstrainedTransform(wout_filepath = self.data['wout_filepath'],
                                                        grid_size=self.data['coarse_grid_size'],
                                                        camera_points_filepath=self.data['camera_filepath'],
                                                        lcf_confined=self.lcf_confined)
        
            self.svd_transform_residuals_u.setup_recon()
            self.svd_transform_residuals_u.run_recon(raw_data = residuals+sigma, raw_data_sigma=sigma, wrapper=2)   
            
            self.svd_transform_residuals_d = ConstrainedTransform(wout_filepath = self.data['wout_filepath'],
                                                        grid_size=self.data['coarse_grid_size'],
                                                        camera_points_filepath=self.data['camera_filepath'],
                                                        lcf_confined=self.lcf_confined)
        
            self.svd_transform_residuals_d.setup_recon()
            self.svd_transform_residuals_d.run_recon(raw_data = residuals-sigma, raw_data_sigma=sigma, wrapper=2)        

        self.combined_grid.update_grid_from_flux_array(self.inv_flux, self.inv_s)
        self.combined_grid.grid['grid_data'] = self.combined_grid.grid['grid_data'] + self.svd_transform_residuals.grid.grid['grid_data']
        return
    
    
    def plot_sim(self, filepath=None):
        if filepath==None:
            print('Specify filepath')
            return
        
        count = self.count
        plt.figure()
        self.fine_grid_sim.plot_grid(title='Simulated Emission: Fine Grid')
        plt.savefig(filepath+str(count)+'_simulated_emission_fine_grid.png', format='png', dpi = 1000,  bbox_inches='tight')
        count += 1
        plt.close()
        
        plt.figure()
        self.coarse_grid_sim.plot_grid(title='Simulated Emission: Fine Grid')
        plt.savefig(filepath+str(count)+'_simulated_emission_coarse_grid.png', format='png', dpi = 1000,  bbox_inches='tight')
        count += 1
        plt.close()        
        
        self.count = count
        return


    def plot_sim_differences(self, filepath=None):
        if filepath==None:
            print('Specify filepath')
            return
        
        count = self.count
        if self.fs_plot >= 1:
            plt.figure()
            self.fine_grid.grid['grid_data'] = self.fine_grid_sim.grid['grid_data'] - self.fine_grid.grid['grid_data']
            self.fine_grid.plot_grid(title='Flux Surface Emission Fit Difference')
            plt.savefig(filepath+str(count)+'_flux_surface_emission_fit_difference.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()
            
        if self.svd_plot >= 1:
            plt.figure()
            self.coarse_grid.grid['grid_data'] = self.coarse_grid_sim.grid['grid_data'] - self.svd_transform.grid.grid['grid_data']
            self.coarse_grid.plot_grid(title='SVD Emission Fit Difference')
            plt.savefig(filepath+str(count)+'_svd_emission_fit_difference.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()     

        if self.residuals_plot >= 1:
            plt.figure()
            self.coarse_grid.update_grid_from_flux_array(self.inv_flux, self.inv_s)
            self.coarse_grid.grid['grid_data'] = self.coarse_grid_sim.grid['grid_data'] - self.coarse_grid.grid['grid_data'] -self.svd_transform_residuals.grid.grid['grid_data']
            self.coarse_grid.plot_grid(title='Residuals SVD Emission Fit Difference')
            plt.savefig(filepath+str(count)+'_residuals_svd_emission_fit_difference.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()            
            
        self.count = count
        return
    
    
    def save_everything(self, filepath=None):
        
        
        if filepath:
            dir1 = filepath
        else:
            dir1 = ''
            
        try:
            os.mkdir(str(dir1 + 'grid_data/'))    
        except:
            pass 
            
        dir1  = str(dir1 + 'grid_data/')
        
        if self.fs_plot >= 1:
            self.fine_grid.update_grid_from_flux_array(self.inv_flux, self.inv_s)
            np.save(str(dir1 + 'fs_fit_grid_data.npy'), self.fine_grid.grid['grid_data'])
            
        if self.fs_plot == 2:
            self.fine_grid.update_grid_from_flux_array(self.inv_flux_sigma_u, self.inv_s)
            np.save(str(dir1 + 'fs_fit_grid_data_u.npy'), self.fine_grid.grid['grid_data'])
            
            self.fine_grid.update_grid_from_flux_array(self.inv_flux_sigma_d, self.inv_s)
            np.save(str(dir1 + 'fs_fit_grid_data_d.npy'), self.fine_grid.grid['grid_data'])        
    
        if self.svd_plot >= 1:
            np.save(str(dir1 + 'svd_fit_grid_data.npy'), self.svd_transform.grid.grid['grid_data'])
            
        if self.svd_plot == 2:
            np.save(str(dir1 + 'svd_fit_grid_data_u.npy'), self.svd_transform_sigma_u.grid.grid['grid_data'])
            np.save(str(dir1 + 'svd_fit_grid_data_d.npy'), self.svd_transform_sigma_d.grid.grid['grid_data'])
         
        if self.residuals_plot >= 1:
            np.save(str(dir1 + 'residuals_fit_grid_data.npy'), self.svd_transform_residuals.grid.grid['grid_data'])
            np.save(str(dir1 + 'combined_fit_grid_data.npy'),  self.combined_grid.grid['grid_data'])

        if self.residuals_plot == 2:
            np.save(str(dir1 + 'residuals_fit_grid_data_u.npy'), self.svd_transform_residuals_u.grid.grid['grid_data'])
            np.save(str(dir1 + 'residuals_fit_grid_data_u.npy'), self.svd_transform_residuals_u.grid.grid['grid_data'])


    def plot_everything(self, filepath=None, signal_name=None):
        if filepath==None:
            print('Specify filepath')
            return
        
        if self.sim_plot:
            label1 = 'Simulated'
        else:
            label1 = signal_name
            
        count = self.count
        
        
        if self.fs_plot >= 1:
            plt.figure()
            self.fine_grid.plot_grid(title='Flux Surface Emission Fit')
            plt.savefig(filepath+str(count)+'_flux_surface_emission_fit.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()
            
            if self.fs_plot == 2:
                self.plot_signal_and_fit(self.signals, self.sigma, self.fs_fitted_signal,
                                         fit_signal_sigma_u = self.fs_fitted_signal_u,
                                         fit_signal_sigma_d = self.fs_fitted_signal_d,
                                         signal_label = label1,
                                         fit_label = 'Fitted Data',
                                         plot_sigma=True,
                                         title = 'Raw Signal vs. Flux Surface Fitted Signals' + ' \n ' + r'$\chi ^2$ = ' + str(self.fs_chi2),
                                         filepath = str(filepath+str(count)+'_raw_signal_vs_flux_surface_fitted_signals.png'))
                count += 1
            else:
                self.plot_signal_and_fit(self.signals, self.sigma, self.fs_fitted_signal,
                                         signal_label = label1,
                                         fit_label = 'Fitted Data',
                                         plot_sigma=False,
                                         title = 'Raw Signal vs. Flux Surface Fitted Signals' + ' \n ' + r'$\chi ^2$ = ' + str(self.fs_chi2),
                                         filepath = str(filepath+str(count)+'_raw_signal_vs_flux_surface_fitted_signals.png'))
                count += 1
                
    
        if self.svd_plot >= 1:
            plt.figure()
            self.svd_transform.grid.plot_grid(title='SVD Emission Fit')
            plt.savefig(filepath+str(count)+'_svd_emission_fit.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()
            
            if self.svd_plot == 2:
                self.plot_signal_and_fit(self.signals, self.sigma, self.svd_fitted_signal,
                                         fit_signal_sigma_u = self.svd_fitted_signal_u,#+self.svd_fitted_signal,
                                         fit_signal_sigma_d = self.svd_fitted_signal_d,#+self.svd_fitted_signal,
                                         signal_label = label1,
                                         fit_label = 'Fitted Data',
                                         plot_sigma=True,
                                         title = 'Raw Signal vs. SVD Fitted Signals' + ' \n ' + r'$\chi ^2$ = ' + str(self.svd_chi2),
                                         filepath = str(filepath+str(count)+'_raw_signal_vs_svd_fitted_signals.png'))
                count += 1
            else:
                self.plot_signal_and_fit(self.signals, self.sigma, self.svd_fitted_signal,
                                         signal_label = label1,
                                         fit_label = 'Fitted Data',
                                         plot_sigma=False,
                                         title = 'Raw Signal vs. SVD Fitted Signals' + ' \n ' + r'$\chi ^2$ = ' + str(self.svd_chi2),
                                         filepath = str(filepath+str(count)+'_raw_signal_vs_svd_fitted_signals.png'))
                count += 1    
                
    
        if self.residuals_plot >= 1:
            plt.figure()
            self.svd_transform_residuals.grid.plot_grid(title='Residuals SVD Emission Fit')
            plt.savefig(filepath+str(count)+'_residuals_svd_emission_fit.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()
            
            if self.residuals_plot == 2:
                self.plot_signal_and_fit(self.residuals, self.sigma, self.residuals_fitted_signal,
                                         fit_signal_sigma_u = self.residuals_fitted_signal_u,
                                         fit_signal_sigma_d = self.residuals_fitted_signal_d,
                                         signal_label = label1,
                                         fit_label = 'Fitted Data',
                                         plot_sigma=True,
                                         title = 'Residuals vs. SVD Fitted Signals'+ ' \n ' + r'$\chi ^2$ = ' + str(self.residuals_chi2),
                                         filepath = str(filepath+str(count)+'_residuals_signal_vs_svd_fitted_signals.png'))
                count += 1
            else:
                self.plot_signal_and_fit(self.residuals, self.sigma, self.residuals_fitted_signal,
                                         signal_label = label1,
                                         fit_label = 'Fitted Data',
                                         plot_sigma=False,
                                         title = 'Residuals vs. SVD Fitted Signals' + ' \n ' + r'$\chi ^2$ = ' + str(self.residuals_chi2),
                                         filepath = str(filepath+str(count)+'_residuals_signal_vs_svd_fitted_signals.png'))
                count += 1        
    
            plt.figure()
            #self.coarse_grid.update_grid_from_flux_array(self.inv_flux, self.inv_s)
            #self.coarse_grid.grid['grid_data'] = self.svd_transform_residuals.grid.grid['grid_data'] + self.coarse_grid.grid['grid_data']
            #self.coarse_grid.plot_grid(title= 'Combined Bolometer Fit')
            self.combined_grid.plot_grid(title='Combined Bolometer Fit')
            plt.savefig(filepath+str(count)+'_combined_flux_surface_and_residuals_svd_emission_fit.png', format='png', dpi = 1000,  bbox_inches='tight')
            count += 1
            plt.close()
            
            self.plot_signal_and_fit(self.signals, self.sigma, self.combined_residuals,
                                     fit_signal_sigma_u = self.residuals_fitted_signal_u + self.fs_fitted_signal_u,
                                     fit_signal_sigma_d = self.fs_fitted_signal_d + self.residuals_fitted_signal_d,
                                     signal_label = label1,
                                     fit_label = 'Fitted Data',
                                     plot_sigma=True,
                                     title = 'Combined Bolometer Fit'+ ' \n ' + r'$\chi ^2$ = ' + str(self.combined_signals_chi2),
                                     filepath = str(filepath+str(count)+'_residuals_combined_signals.png'))
            count += 1    
            
        self.count = count
        return
    
    
    def plot_signal_and_fit(self, signal, sigma, fit_signal, fit_signal_sigma_u, fit_signal_sigma_d, 
                            signal_label=None, fit_label=None, plot_sigma=False,
                            title = None, filepath=None):
        x= np.linspace(1, len(signal), len(signal))
        plt.figure()
        plt.plot(x, signal, label=signal_label, color='k')
        plt.plot(x, fit_signal, label=fit_label, color='r')
        
        if plot_sigma:
            plt.fill_between(x,signal+sigma, signal-sigma, color='k', alpha=.3)
            plt.fill_between(x,fit_signal_sigma_u, fit_signal_sigma_d, color='r', alpha=.3)

        plt.title(title, fontsize =15, weight='bold')
        plt.xlabel('Channel Number',fontsize = 15, weight ='bold')
        plt.ylabel('Relative Intensity',fontsize = 15, weight ='bold')
        plt.xticks(fontsize=13,weight='bold')
        plt.yticks(fontsize=13,weight='bold')
        legend_properties = {'weight':'bold',
                             'size' : 13}
        plt.legend(loc=4, prop=legend_properties) 
        
        if filepath:
            plt.savefig(filepath, format='png', dpi = 1000,  bbox_inches='tight')
            plt.close()
    
    
    def fft_grid(self, grid=None):
        grid.get_s_theta_points()
        s_theta_array = grid.s_theta_array
        
        theta = grid.theta
        
        fft_master = []
        
        s = grid.s
        N = len(theta)
        theta = np.linspace(0, 1, N)
        step = theta[1] - theta[0]
        freq = np.linspace(0, 1/step, N)
        
        
        
        for kk, row in enumerate(s_theta_array):
            row_fft = np.fft.rfft(row)
            #for ii in range(len(r ow_fft)):
            #    if freq[ii]<=fft_bounds[0] or freq[ii] >= fft_bounds[1]:
            #        row_fft[ii] = 0
                
            fft_master.append(row_fft)
            
        
        return fft_master, freq, s, N
    
    
    def filter_grid(self, grid=None, noise_fft_bounds = [-1,10], 
                    plot_fft = True, cutoff = 0.02,
                    filepath=None, save=True, plot_new_grid=True,
                    plot_ind_freq=True):
        
        
        try:
            os.mkdir(str(filepath + 'fft/'))
        except:
            pass
        
        filepath = str(filepath + 'fft/')
        
        fft_m, freq, s, N = self.fft_grid(grid=grid)
        
        fft_m_sum = sum(fft_m)
        

        
        new_grid = []
        for kk, row in enumerate(fft_m):
            for ii in range(len(row)):
                if fft_m_sum[ii] < cutoff * max(fft_m_sum):
                    row[ii] = 0
                
                
                if freq[ii]<=noise_fft_bounds[0] or freq[ii] >= noise_fft_bounds[1] :
                    
                    row[ii] = 0
                    
            new_grid.append(np.fft.irfft(row))
        
        #print(np.array(new_grid).shape)
        grid.update_grid_from_s_theta_array(np.array(new_grid))
        
        if plot_new_grid:
            plt.figure()
            grid.plot_grid(title='Filtered Grid')
            if save:
                plt.savefig(str(filepath)+'filtered_grid_' +str(noise_fft_bounds[0]) + '_' + 
                            str(noise_fft_bounds[1]) +'.png', format='png', dpi = 1000,  bbox_inches='tight')
                plt.close()

        
        if save:
            np.save(str(filepath)+'fft.npy', fft_m)
            np.save(str(filepath)+'fft_freq.npy', freq)
            np.save(str(filepath)+'filtered_grid_' +str(noise_fft_bounds[0]) + '_' +
                    str(noise_fft_bounds[1]) + '.npy', new_grid)
            
        
        #freq = freq[:N//2]
        #
        #fft_m = fft_p[:,:-1]
        fft_p = np.array(fft_m[:N//2])*1/N
        fft_p_sum = np.abs(fft_m_sum)[:N//2]*1/N
        h_freq = freq[:N//2]
        
        #print(len(h_freq), len(fft_p_sum))
        values = np.array(np.abs(fft_p_sum)).argsort()[-10:][::-1]
        #print(values)
        
        fil_values = []
        for value in values:
            if value > noise_fft_bounds[0] and value < noise_fft_bounds[1]:
                fil_values.append(value)
                    
        values = np.array(fil_values)
        #values = np.array([value in values if (value > noise_fft_bounds[0]) and (value < noise_fft_bounds[1])])
        ind1 = find_closest_index(h_freq, noise_fft_bounds[0])
        ind2 = find_closest_index(h_freq, noise_fft_bounds[1])
        #print(ind1,ind2)
        
           
        if plot_ind_freq:
            count = 0
            try:
                os.mkdir(str(filepath + 'individual/'))
            except:
                print('Folder made')
            
            
            
            
            filepath2 = str(filepath + 'individual/')
            
            ind_new_grid_master = []
            for ind in values:
                ind_new_grid = []
                empty_fft = np.zeros(np.array(fft_p).shape,dtype=np.complex_)
                for ii in range(len(fft_p)):
                    empty_fft[ii][ind] = fft_p[ii][ind]
                    #print(ind, fft_p_sum[ind], fft_p[ii][ind])
                    ind_new_grid.append(np.fft.irfft(empty_fft[ii]))
                ind_new_grid_master.append(ind_new_grid)    
                

            for jj, ind in enumerate(values):
            #for jj, grid_i in enumerate(ind_new_grid_master):
                freq_string = str(round(h_freq[ind],2))
                amp_string = str(round(np.abs(fft_p_sum[ind]),2))
                plt.figure()
                grid.update_grid_from_s_theta_array(np.array(ind_new_grid_master[jj]))
                title = str('Fourier Grid Component \n Frequency: ' 
                            + freq_string + '    Amplitude: ' 
                            + amp_string)
                grid.plot_grid(title=title)
                if save:
                    plt.savefig(str(filepath2)+str(count)+'_fft_component_grid_freq_' + freq_string +'_amp_' + amp_string+ '.png', 
                                format='png', dpi = 1000,  bbox_inches='tight')
                    #print('Why')
                    plt.close()     
                count += 1    
                
        if plot_fft:
            fig = plt.figure()
            plt.subplot(211)
            
            
            
            title2 = 'Fourier Analysis'
            plt.title(title2, fontsize =15, weight='bold')
            plt.bar(h_freq, fft_p_sum)
            plt.xlim([-.5, noise_fft_bounds[1]+.5])
            plt.yticks(fontsize=13,weight='bold')
            plt.ylabel('Amplitude',fontsize = 15, weight ='bold')            
            #plt.xticks(np.arange(min(f[:N//2]), max(f[:N//2])+1, 1))
            plt.gca().axes.get_xaxis().set_visible(False)
            
            
            
            
            plt.subplot(212)
            pcon = plt.pcolormesh(h_freq-.5,s,np.abs(fft_p[:,:-1]), cmap='gnuplot2')
            plt.xticks(np.arange(min(h_freq), max(h_freq)+1, 1))
            plt.xlim([-.5, noise_fft_bounds[1] + .5])
            plt.xlabel('Frequency',fontsize = 15, weight ='bold')
            plt.ylabel('s',fontsize = 15, weight ='bold')
            plt.xticks(fontsize=13,weight='bold')
            plt.yticks(fontsize=13,weight='bold')
            
            
            cbaxes = fig.add_axes([0.95, 0.11, 0.05, .35])
            cbar = plt.colorbar(pcon, cax = cbaxes)
            labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
            cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')            
            cbar.set_label('Amplitude', rotation=270,fontsize=13, weight='bold',labelpad=15)
            
            if save:
                plt.savefig(str(filepath)+'fft_spectrum.png', 
                            format='png', dpi = 1000,  bbox_inches='tight')
                plt.close()    
                
            fig = plt.figure()
            plt.subplot(211)
            
            
            
            title2 = 'Fourier Analysis'
            plt.title(title2, fontsize =15, weight='bold')
            plt.bar(h_freq[1:], fft_p_sum[1:])
            plt.xlim([.5, noise_fft_bounds[1] +.5])
            plt.yticks(fontsize=13,weight='bold')
            plt.ylabel('Amplitude',fontsize = 15, weight ='bold')            
            #plt.xticks(np.arange(min(f[:N//2]), max(f[:N//2])+1, 1))
            plt.gca().axes.get_xaxis().set_visible(False)
            
            
            
            
            plt.subplot(212)
            pcon = plt.pcolormesh(h_freq[1:]-.5,s,np.abs(fft_p[:,1:-1]), cmap='gnuplot2')
            plt.xticks(np.arange(min(h_freq), max(h_freq)+1, 1))
            plt.xlim([.5, noise_fft_bounds[1]+.5])
            plt.xlabel('Frequency',fontsize = 15, weight ='bold')
            plt.ylabel('s',fontsize = 15, weight ='bold')
            plt.xticks(fontsize=13,weight='bold')
            plt.yticks(fontsize=13,weight='bold')
            
            
            cbaxes = fig.add_axes([0.95, 0.11, 0.05, .35])
            cbar = plt.colorbar(pcon, cax = cbaxes)
            labels = [item.get_text() for item in cbar.ax.get_yticklabels()]
            cbar.ax.set_yticklabels(labels,fontsize=13, weight='bold')            
            cbar.set_label('Amplitude', rotation=270,fontsize=13, weight='bold',labelpad=15)
            
            if save:
                plt.savefig(str(filepath)+'fft_spectrum_without_0.png', 
                            format='png', dpi = 1000,  bbox_inches='tight')
                plt.close()  
                
    