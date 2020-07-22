# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:48:54 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import sys
sys.path.insert(0, '/home/cth/cthgroup/Python/recon')

from recon_input import InputClass
import click
import numpy as np
 


# =============================================================================
# Example Commandline Use: python recon_runner.py shot 'times'
#                          python recon_runner.py 14092626 '1.62 1.63 1.64'
#                          
# Input files will be saved in shot_number directory that is in the 
# working_directory set below.
# =============================================================================

           
@click.command(context_settings=dict(ignore_unknown_options=True,
                                     allow_extra_args=True,))  
@click.pass_context
@click.argument('shotnumber')
@click.argument('start_time')
@click.argument('end_time')
@click.argument('number_of_recons')
@click.option('--inputs', is_flag=True, help='Generates input files only')
@click.option('--fastest', is_flag=True, help='Run V3Fit and use output of one run for input of next run')
@click.option('--reverse', is_flag=True, help='Reverse the order the input files are run (go backwards in time)')


def cmd_line(ctx, shotnumber, start_time, end_time, number_of_recons, 
             inputs, fastest, reverse):
    
    d = dict()
    for item in ctx.args:
        d1 = [item.split('=')]
        d.update(d1)
    
    start = float(start_time)
    end = float(end_time)
    n_times = int(number_of_recons)
    
    times_a = np.linspace(start, end, n_times)
    times = []
    
    for time in times_a:
        times.append(round(time, 4))


    try:
        with open('v3config.txt', 'r') as file:
            lines = file.readlines()
        marker = True
    except:
        
        marker = False
        
    if marker:
        for i, line in enumerate(lines):
            if line.startswith('working_directory'):
                working_directory1 = line.rstrip().split('=')[1]
            elif line.startswith('vmec_template'):
                vmec_template1 = line.rstrip().split('=')[1]                
            elif line.startswith('v3fit_template'):
                v3fit_template1 = line.rstrip().split('=')[1]
            elif line.startswith('v3fit_executable'):
                v3fit_executable1 = line.rstrip().split('=')[1]            
        
        if 'v3fit_executable' not in d:
            d['v3fit_executable']=v3fit_executable1
        if 'directory' not in d:
            d['directory']=working_directory1
        if 'vmec_template' not in d:
            d['vmec_template']=vmec_template1
        if 'v3fit_template' not in d:
            d['v3fit_template']=v3fit_template1            

        
        shot = InputClass(int(shotnumber), times, 
                          **d)
    else:    
        shot = InputClass(int(shotnumber), times, **d)
        
    if fastest:
        if reverse:
            shot.generate_and_run_fastest(reverse_order=True)
        else:
            shot.generate_and_run_fastest()
    elif inputs:
        shot.generate_input_files()
    else:
        shot.generate_and_run()

        
if __name__ == '__main__':
    cmd_line()    