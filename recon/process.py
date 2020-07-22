# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:02:09 2019

@author: James Kring
@email:  jdk0026@auburn.edu
"""
import os
import sys
sys.path.insert(0, '/home/cth/cthgroup/Python/recon/scripts')



from v3fit_util import *
from v3fit_database import *
from vmec import wout_file
from result_file import result_file



def get_iota_vac(shot,inter):
    single_recon = '/home/inst/jdk0026/reconstructions/single_recon/'

    dir_path = str(single_recon + str(shot) + '/1.61/' + str(inter) + '/')
    

    if os.path.isdir(dir_path):
        path = str(dir_path + 'wout_'+str(shot)+'_1.61_0.vmec.nc')
        
        if os.path.exists(path):
            wout = wout_file(path)
                           
    return wout.iotaf.data.tolist()



def grab_recon_data(shot):
    times, AC, AM, iota, raw_density, raw_plasma_current =[], [], [], [], [], []
    curtor, pp_ne_as, pp_ne_af, pp_sxrem_as, pp_sxrem_af1, pp_sxrem_af2 = [], [], [], [], [], []
    prescale, z_offset, phiedge, rmnc, zmns, xm, xn, chi_squared = [], [], [], [], [], [], [], []
    s, Rmajor, Aminor, sxr, bolo, wout_location, volume_p = [], [], [], [], [], [], []
    
    try:
        iota_vac = get_iota_vac(shot, 0)
    except:
        try:
            iota_vac = get_iota_vac(shot, 1)
        except:
            print('Iota_vac failed')    
            iota_vac = None 


    rows = select_recon_by_shotnumber_and_fs_id(shot, fs_id=None)
    
    #rows = [rows[-1]]
    
    times = []
    
    for row in rows:
        try:
            shot,time,window,full_shot,location = row
            print(shot, time, location)
            woutname    = [f for f in os.listdir(location) if f.startswith('wout')][0]
            recoutname  = [f for f in os.listdir(location) if f.startswith('result')][0]
            
            #print('Here',1)
            #print(location)
            #print(woutname)            
            
            wout_location.append(str(location + woutname))
            
            wout    = wout_file(str(location + woutname))
            #print('Here',1.1)  

            recout  = result_file(str(location + recoutname), True)        
            #print('Here',1.2)           
            times.append(time)

            ac_ind = get_param_index(recout,'ac')
            
            AC.append([[recout.param_value[ac_ind], recout.param_value[ac_ind + 1]],
                       [recout.param_sigma[ac_ind], recout.param_sigma[ac_ind + 1]]])


            am_ind = get_param_index(recout,'am')
            
            AM.append([[recout.param_value[am_ind], 6.0],[recout.param_value[am_ind],0]])
            
            iota.append(wout.iotaf.data.tolist())
            
            raw_density.append(get_channel_average(shot, 'processed:intfrm_1mm:int_nedl_1', time, window*.5))
            
            raw_plasma_current.append(get_channel_average(shot, '\I_P', time, window*.5))

            curtor.append(0)
            pp_ne_as.append([0.0, 0.6, 1.0, 1.5])
            
            ne_ind = get_param_index(recout,'pp_ne_af')
            pp_ne_af.append([[recout.param_value[ne_ind], recout.param_value[ne_ind + 1], 0.0, 0.0],[recout.param_sigma[ne_ind], recout.param_sigma[ne_ind + 1], 0.0, 0.0]])
        
            pp_sxrem_as.append([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1 ])
        
            sxr_ind = get_param_index(recout, 'pp_sxrem_af_a')
            try:
                pp_sxrem_af1.append([[recout.param_value[sxr_ind+0],recout.param_value[sxr_ind+1],recout.param_value[sxr_ind+2],recout.param_value[sxr_ind+3],
                                      recout.param_value[sxr_ind+4],recout.param_value[sxr_ind+5],recout.param_value[sxr_ind+6],recout.param_value[sxr_ind+7],
                                      recout.param_value[sxr_ind+8],recout.param_value[sxr_ind+9]],
                                    [recout.param_sigma[sxr_ind+0],recout.param_sigma[sxr_ind+1],recout.param_sigma[sxr_ind+2],recout.param_sigma[sxr_ind+3],
                                     recout.param_sigma[sxr_ind+4],recout.param_sigma[sxr_ind+5],recout.param_sigma[sxr_ind+6],recout.param_sigma[sxr_ind+7],
                                     recout.param_sigma[sxr_ind+8],recout.param_sigma[sxr_ind+9]]])
    
                pp_sxrem_af2.append([[recout.param_value[sxr_ind+10],recout.param_value[sxr_ind+11],recout.param_value[sxr_ind+12],recout.param_value[sxr_ind+13],
                                      recout.param_value[sxr_ind+14],recout.param_value[sxr_ind+15],recout.param_value[sxr_ind+16],recout.param_value[sxr_ind+17],
                                      recout.param_value[sxr_ind+18],recout.param_value[sxr_ind+19]],
                                    [recout.param_sigma[sxr_ind+10],recout.param_sigma[sxr_ind+11],recout.param_sigma[sxr_ind+12],recout.param_sigma[sxr_ind+13],
                                     recout.param_sigma[sxr_ind+14],recout.param_sigma[sxr_ind+15],recout.param_sigma[sxr_ind+16],recout.param_sigma[sxr_ind+17],
                                     recout.param_sigma[sxr_ind+18],recout.param_sigma[sxr_ind+19]]])   
            except:
                pass

            pre_ind = get_param_index(recout, 'pres_scale')
            prescale.append([recout.param_value[pre_ind],recout.param_sigma[pre_ind]])

            zoff_ind= get_param_index(recout, 'z_offset')
            z_offset.append([recout.param_value[zoff_ind], recout.param_sigma[zoff_ind]])

            phi_ind = get_param_index(recout, 'phiedge')
            phiedge.append([recout.param_value[phi_ind], recout.param_sigma[phi_ind]])

            rmnc.append(wout.rmnc.tolist())
            zmns.append(wout.zmns.tolist())
            xm.append(wout.xm.tolist())
            xn.append(wout.xn.tolist())

            chi_squared.append(float(recout.g2[-1]))

            s.append(wout.s.tolist())
            

            Rmajor.append(wout.Rmajor.data.tolist())
            Aminor.append(wout.Aminor.data.tolist())
            volume_p.append(wout.volume_p.data.tolist())

            #sxr.append(get_sxr_cameras(shot, time, window*.5))

            #bolo.append(get_bolo_cameras(shot, time, window*.5))

            
            print('Success')
        except:
            print('Data Grab Failed')
    
    try:
        sxr = get_sxr_cameras(shot, times, window*.5, pad_times=False)
        bolo = get_bolo_cameras(shot, times, window*.5, pad_times=False)
    except:
        print('SXR and Bolo not grabbed')

    #print(rmnc)
    results_to_database(shot, 'fermi_dirac', 'two_power', times, AC, AM, iota_vac,
                        iota, raw_density, raw_plasma_current, curtor, pp_ne_as,
                        pp_ne_af, pp_sxrem_as, pp_sxrem_af1, pp_sxrem_af2,
                        prescale, z_offset, phiedge, rmnc, zmns, xm, xn,
                        chi_squared, s, Rmajor, Aminor, sxr, bolo, wout_location, 
                        volume_p)
    
    


def main(shot):
    
    #shots = get_recon_shotnumbers()
    
    shots = [[shot]]
    #for i in range(0, 1):
    for i in range(0, len(shots)):
        shot = int(shots[i][0])
        grab_recon_data(shot)