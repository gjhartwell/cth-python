# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 10:27:53 2020

@author: James Kring
@email:  jdk0026@auburn.edu
"""
from cth_bolometer_inversion import CTHBolometerInversion
import time as t
import numpy as np
import os
import sys
#rows = select_recon_by_shotnumber_and_fs_id(19101127)
from v3fit_database import generic_query_results, ReconResults

#main(19101127)

def main(shot, pad_times=False):
    t1 = t.time() 


    query= "SELECT * FROM results WHERE shot=?"
    r1 = ReconResults(query,  (int(shot),))
    r1.select_results(query, (int(shot),))


    """
    plt.figure()
    #plt.plot(r1.times, np.array(r1.raw_density)[:,0])
    #plt.plot(r1.times, r1.raw_plasma_current)
    
    
    
    up = np.array(r1.sxr)[30,:,0] + np.array(r1.sxr)[30,:,1]
    down = np.array(r1.sxr)[30,:,0] - np.array(r1.sxr)[30,:,1]
    
    plt.plot(r1.times, np.array(r1.sxr)[30,:,0],'k')
    plt.fill_between(r1.times, up, down, color='r', alpha=.3)
    """
    points_path = '/home/cth/cthgroup/Python/recon/scripts/SC252_points.npy'
    dir_master = '/home/cth/cthgroup/_Users/Kring/inverted_shots/'
        
    shot_path = str(dir_master + str(int(r1.shot)) +'/')
        
    if os.path.isdir(shot_path):
        print('Shot Path Exists')  
    else:
        os.mkdir(shot_path)
            
    try:
        max_count = max(int([x[0] for x in os.walk(shot_path)])) +1
    except:
        max_count = 0
    
    shot_iter_path = str(shot_path + str(max_count) +'/')
    
    try:
        os.mkdir(shot_iter_path)
    except:
        print('Shot Iteration Path Exists')


    results = {}
    results['times'] = []

    print('Times',len(r1.times))

    if pad_times:
        times = r1.times
        window = times[1] -times[0]
        step = window/5
        
        new_times = []
        for time in times:
            for ii in range(0,5):
                new_times.append(time+ii*step)
                
        r1.times = np.array(new_times)
        
        

    for ii, time in enumerate(r1.times):
        results['times'].append(time)    
        plot_path = str(shot_iter_path + str(time) +'/')
        try:
            os.mkdir(plot_path)
        except:
            print('Plot Path Exists')

        if pad_times:
            wout_filepath = str(r1.wout_location[ii//5])
        else:
            wout_filepath = str(r1.wout_location[ii])
        
        # Initialize the Inversion

    
        inv1 = CTHBolometerInversion(wout_filepath=wout_filepath,
                                     camera_points_filepath=points_path,
                                     lcf_confined=False)
        
        print('Bolo',np.array(r1.bolo).shape)
        
        
        sim_data = np.array(r1.bolo)[:,ii,0]
        sim_sigma = np.array(r1.bolo)[:,ii,1]
        
        print('Data',sim_data.shape)
        
        # Begin Inversion
        
        inv1.flux_surface_fit(sim_data, sim_sigma, estimate_uncertainty=True)
        inv1.svd_fit(sim_data, sim_sigma, estimate_uncertainty=True)

        residual_signal = sim_data - inv1.fs_fitted_signal
        
        
        inv1.residuals_fit(residual_signal, sim_sigma, estimate_uncertainty=True)
        
        
        print("Took " + str(round(t.time() - t1, 4)) + ' sec: Inversion Time' )
        # Plot results
        inv1.plot_everything(filepath=plot_path, signal_name='Raw Data')
        inv1.save_everything(filepath=plot_path)
        
        print("Took " + str(round(t.time() - t1, 4)) + ' sec: Total Time' )
        
        
        inv1.filter_grid(grid = inv1.combined_grid, filepath=plot_path, 
                         plot_ind_freq=True, noise_fft_bounds=[-1, 50])

