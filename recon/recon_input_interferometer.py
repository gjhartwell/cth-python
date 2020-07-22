# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 08:47:03 2018

@author: James Kring
@email:  jdk0026@auburn.edu
"""

import numpy as np
from v3data import V3Data
import subprocess
import os
from netCDF4 import Dataset
FNULL = open(os.devnull, 'w')



class InputClass:
    def __init__(self, shotnumber, times, 
                 time_window_average = 0.0001,
                 directory = '',
                 vmec_template='/home/cth/cthgroup/Python/recon/input_example/input.example.vmec', 
                 v3fit_template='/home/cth/cthgroup/Python/recon/input_example/input.interferometer_only.v3fit',
                 NS_ARRAY=15,
                 AC=[1.0, 3.0, 6.0],#[1.0, 12.0, 10.0], 
                 PCURR_TYPE='two_power',#'fermi_dirac',
                 AM=[1.0, 1.5, 6.0], 
                 pmass_type='two_power',
                 v3fit_executable='xv3fit_kring',
                 diagnostic_count = [0, 0, 4]):  #mag, sxr/bolo, intfrm
        self.data = {}
        self.data['shot number'] = shotnumber
        self.data['times'] = times                        # in seconds
        self.data['time window'] = time_window_average    # in seconds
        
        self.data['NS_ARRAY'] = NS_ARRAY
        self.data['AC'] = self.kwarg_string_to_array(AC)
        self.data['PCURR_TYPE'] = PCURR_TYPE
        self.data['AM'] = self.kwarg_string_to_array(AM)
        self.data['pmass_type'] = pmass_type
        self.data['directory'] = directory
        self.data['diagnostic_count'] = self.kwarg_string_to_array(diagnostic_count)
        self.dir_rel_to_abs()
        
        self.vmec_temp = vmec_template
        self.v3fit_temp = v3fit_template

        self.shot = V3Data(self.data['shot number'])
        self.v3_exe = v3fit_executable
        self.counter= 0
        #self.save_data()

    def kwarg_string_to_array(self, kwarg):
        if isinstance(kwarg, str):
            kwarg = kwarg.rstrip(']').lstrip('[').split(',')
            kwarg = [float(value) for value in kwarg]
        return kwarg
        
        
    def decode_nc_string(self, nc_array):
        new_array = []
    
        for item in nc_array:
            item_array = []
            for sub_item in item:
                decoded_sub_item = sub_item.decode("utf-8")
                item_array.append(decoded_sub_item)
            
            new_item = ''.join(item_array)
            new_array.append(new_item.rstrip())
        
        return new_array

    
    def dir_rel_to_abs(self):
        if self.data['directory'].startswith('~'):
            old_dir = self.data['directory']
            home = os.path.expanduser("~")
            new_dir = str(home + old_dir[1:])
            self.data['directory'] = new_dir

    
    def find_closest_index(self, array, value):
        new_array = abs(array - value)
        try:
            index = new_array.argmin()
        except:
            print('Invalid Array')
            index = 0    
        return int(index)
        
    
    def average_window(self, data_array, time_array, time, window, absolute=False):
        time = time
        ind1 = self.find_closest_index(time_array, time - window)
        ind2 = self.find_closest_index(time_array, time + window)
        
        ave_data = []
        sig_data = []
        
        for data in data_array:
            if absolute:
                value = np.mean(abs(data[ind1:ind2]))
                sigma = np.std(abs(data[ind1:ind2]),ddof=1)
            else:
                value = np.mean(data[ind1:ind2])
                sigma = np.std(data[ind1:ind2],ddof=1)
            ave_data.append(value)
            sig_data.append(sigma)
        
        
        return ave_data, sig_data
        

    
    def grab_data(self):
        mag_count = int(self.data['diagnostic_count'][0])
        sxr_count = int(self.data['diagnostic_count'][1])
        int_count = int(self.data['diagnostic_count'][2])
        
        cur_data, cur_time = self.shot.raw_currents()  
        print('> Currents Grabbed')
        pre_data, pre_time = self.shot.raw_pressure()
        print('> Pressure Scaled')
        
        if mag_count!=0:
            mag_data, mag_time = self.shot.raw_magnetics()
            print('> Magnetics Calibrated')
        if sxr_count!=0:
            try:
                sxr_data, sxr_time = self.shot.raw_sxr()
                print('> SXR Cameras Observed')
            except:
                print('> SXR Cameras Skipped')  
        if int_count!=0:    
            int_data, int_time = self.shot.raw_density()
            print('> Density Determined')

        master = []
        half_window = self.data['time window'] *.5
        
        sig_master =[]
        
        
        for time in self.data['times']:
            sub = []
            sub.append(time)            
            sig_sub = [] 
            sig_sub.append(time)
            try:
                sub.append(self.average_window(cur_data, cur_time, time, half_window)[0])
                sig_sub.append(self.average_window(cur_data, cur_time, time, half_window)[1])
            except:
                print('Coil Currents not Averaged')
                return
            try:
                sub.append(self.average_window(pre_data, pre_time, time, half_window)[0])
                sig_sub.append(self.average_window(pre_data, pre_time, time, half_window)[1])
            except:
                print('Pressure not Averaged')
                return
            try:
                sub.append(self.average_window(mag_data, mag_time, time, half_window)[0])
                sig_sub.append(self.average_window(mag_data, mag_time, time, half_window)[1])
            except: 
                pass
            try:
                sub.append(self.average_window(sxr_data, sxr_time, time, half_window*6)[0])
                sig_sub.append(self.average_window(sxr_data, sxr_time, time, half_window*6)[1])
            except:
                pass
            try:
                sub.append(self.average_window(int_data, int_time, time, half_window)[0])
                sig_sub.append(self.average_window(int_data, int_time, time, half_window)[1])
            except:
                pass
            
            master.append(sub)
            sig_master.append(sig_sub)            
   
        return master, sig_master
        
        
    def data_to_vmec(self, master, new_vmec):
        file = open(self.vmec_temp, 'r')
        
        lines = file.readlines()
        file.close()
                    
        #new_vmec = str('input.' + str(self.data['shot number']) +'_' +
        #                   str(master[0]) + '_' + str(self.counter) + '.vmec')
        print('> ' + new_vmec)
        
        for i,line in enumerate(lines):
            if line.startswith('NS_ARRAY'):
                ns_ind = i
            elif line.startswith('EXTCUR'):
                extcur_ind = i
            elif line.startswith('PHIEDGE'):
                phi_ind = i
            elif line.startswith('RBC(0,0)'):
                rbc_ind1= i
                rbc_ind2= rbc_ind1 + 1
            elif line.startswith('ZBS(0,0)'):
                zbs_ind1= i
                zbs_ind2= zbs_ind1 + 1
            elif line.startswith('CURTOR'):
                curtor_ind = i
            elif line.startswith('PRES_SCALE'):
                pres_ind = i
            elif line.startswith('AC'):
                ac_ind = i
            elif line.startswith('AM'):
                am_ind = i
            elif line.startswith('PCURR_TYPE'):
                pc_ind = i
                
        lines[ns_ind] = 'NS_ARRAY = ' + str(self.data['NS_ARRAY'])+', \n'
        lines[extcur_ind] = str('EXTCUR =' + 
                                str(master[1][1]) + ', ' + #HF
                                str(master[1][2]) + ', ' + #TVF
                                str(master[1][3]) + ', ' + #OH
                                str(master[1][4]) + ', ' + #SVF
                                str(master[1][5]) + ', ' + #RF
                                str(master[1][6]) + ', ' + #TF
                                str(master[1][7]) + ', ' + #VV
                                str(master[1][8]) + ', \n') #HCF
        lines[phi_ind] = str('PHIEDGE = ' + str(-1*master[1][9]) + ',\n')
        #lines[rbc_ind1]= str('RBC(0,0) = '+ str(master[1][10])+ ',\n')
        #lines[rbc_ind2]= str('RBC(0,1) = '+ str(master[1][11])+ ',\n')
        #lines[zbs_ind1]= str('ZBS(0,0) = '+ str(master[1][12])+ ',\n')
        #lines[zbs_ind2]= str('ZBS(0,1) = '+ str(master[1][13])+ ',\n')
        lines[curtor_ind] = str('CURTOR = '+ str(master[1][0])+ ',\n')
        #print(str('CURTOR = '+ str(master[1][0])+ ',\n'))
        lines[pres_ind]= str('PRES_SCALE = ' + str(master[2][0])+',\n')
        lines[ac_ind]  = str('AC = ' + str(self.data['AC'][0]) + ', ' 
                             + str(self.data['AC'][1]) +', ' 
                             + str(self.data['AC'][2]) + ',\n')
        lines[am_ind]  = str('AM = ' + str(self.data['AM'][0]) + ', ' 
                             + str(self.data['AM'][1]) +', ' 
                             + str(self.data['AM'][2]) + ',\n') 
        lines[pc_ind] = str("PCURR_TYPE = '" + self.data['PCURR_TYPE'] + "',\n")                
        with open(new_vmec, 'w') as file2:
            for line in lines:
                file2.write(line)
                      
        return
    
    
    def data_to_v3fit(self, master, sig_master, new_vmec, new_v3fit):
        file = open(self.v3fit_temp, 'r')
        
        lines = file.readlines()
        file.close()    

        print('> ' + new_v3fit)
        
        data_ind_array = []
        sigma_ind_array = []
        
        

        for i,line in enumerate(lines):
            if line.startswith('sdo_data'):
                data_ind_array.append(i)
            elif line.startswith('sdo_sigma'):
                sigma_ind_array.append(i)
            elif line.startswith('vmec_nli_filename'):
                vmec_ind = i
            elif line.startswith('n_sdata_o'):
                data_count_ind = i
                

        mag_count = int(self.data['diagnostic_count'][0])
        sxr_count = int(self.data['diagnostic_count'][1])
        int_count = int(self.data['diagnostic_count'][2])

        ii = 0
        j = 3
        if mag_count==0:
            mag_ind = None
        else:
            mag_ind = data_ind_array[ii]
            mag_sig_ind = sigma_ind_array[ii]
            ii+=1
            mag_list = master[j]
            mag_string = str(str(mag_list[0]) + ', ')
            for i in range(1, len(mag_list)-1):
                mag_string += str(str(mag_list[i]) + ', ')
            mag_string += str(str(mag_list[-1]) + ', \n')       

            mag_sig_list = sig_master[j]
            mag_sig_string = str(str(mag_sig_list[0]) + ', ')
            for i in range(1, len(mag_sig_list)-1):
                mag_sig_string += str(str(mag_sig_list[i]) + ', ')
            mag_sig_string += str(str(mag_sig_list[-1]) + ', \n')
            j+=1
            
        if sxr_count==0:
            sxr_ind = None
        else:
            sxr_ind = data_ind_array[ii]
            sxr_sig_ind = sigma_ind_array[ii]
            ii+=1
            sxr_list = master[j]
            sxr_string = str(str(sxr_list[0]) + ', ')
            for i in range(1, sxr_count-1):
                sxr_string += str(str(sxr_list[i]) + ', ')
            sxr_string += str(str(sxr_list[-1]) + ', \n')
        
            sxr_sig_list = sig_master[j]
            sxr_sig_string = str(str(sxr_sig_list[0]) + ', ')
            for i in range(1, sxr_count-1):
                sxr_sig_string += str(str(sxr_sig_list[i]) + ', ')
            sxr_sig_string += str(str(sxr_sig_list[-1]) + ', \n')
            j+=1
            
        if int_count==0:    
            int_ind = None
        else:
            int_ind = data_ind_array[ii]
            int_sig_ind = sigma_ind_array[ii]
            ii+=1
            int_list = master[j]
            int_string = str(str(int_list[0]) + ', ')
            for i in range(1,int_count-1):
                int_string += str(str(int_list[i]) + ', ')
            int_string += str(str(int_list[-1]) + ', \n')
                
        
            int_sig_list = sig_master[j]
            int_sig_string = str(str(int_sig_list[0]) + ', ')
            for i in range(1, int_count-1):
                int_sig_string += str(str(int_sig_list[i]) + ', ')
            int_sig_string += str(str(int_sig_list[-1]) + ', \n')     
        
            j+=1
            
        
        
        
        
        try:
            lines[vmec_ind] = "vmec_nli_filename = '" + new_vmec +"',\n"
        except:
            pass
        try:
            lines[mag_ind]  = 'sdo_data_a(1:' +str(mag_count) +') = ' + mag_string
            lines[mag_sig_ind]  = 'sdo_sigma_a(1:' +str(mag_count) +') = ' + mag_sig_string
        except:
            pass
        try:
            lines[sxr_ind]  = 'sdo_data_a('+str(mag_count+1) +':' +str(mag_count+sxr_count)+') = ' + sxr_string
            lines[sxr_sig_ind]  = 'sdo_sigma_a('+str(mag_count+1) +':' +str(mag_count+sxr_count)+') = ' + sxr_sig_string
        except:
            pass
        try:
            lines[int_ind]  = 'sdo_data_a('+str(mag_count+sxr_count+1) +':' +str(mag_count+sxr_count+int_count)+') = ' + int_string        
            lines[int_sig_ind]  = 'sdo_sigma_a('+str(mag_count+sxr_count+1) +':' +str(mag_count+sxr_count+int_count)+') = ' + int_sig_string
        except:
            pass

        try:
            lines[data_count_ind]  = str('n_sdata_o = ' + str(mag_count+sxr_count+int_count+6)+', \n')
        except:
            pass
        
        with open(new_v3fit, 'w') as file2:
            for line in lines:
                file2.write(line)
                            
        return new_v3fit    
    
    
    def create_dir_and_mv(self, input_list):
        # This function will first check for to see what directories currently 
        # exist in order to know what directories need to be made.
        # Some of the command line processes are redundant in order to ensure
        # that everything is placed correctly.
        
        try:
           com = str('cd ' + self.data['directory'])
           subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        except:
            print('Error: Directory ' + self.data['directory'] + ' does not exist')
            
        try:
           com = str('cd ' + self.data['directory'] + 
                     '&& mkdir ' + str(self.data['shot number']))
           subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        except:
            pass
            
        try:
           com = str('cd ' + self.data['directory'] + str(self.data['shot number']))
           subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
        except:
            print('Error: ' +str(self.data['shot number']) + ' may not exist')
            
        

        
        for i in range(len(input_list)):   
            shot_dir = str(self.data['directory'] + str(self.data['shot number'])+ '/')


            try:
                com = 'cd ' + shot_dir + '&& mkdir ' + str(self.data['times'][i])
                subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
            except:
                pass
            
            shot_dir = str(self.data['directory'] + str(self.data['shot number'])+ '/' + str(self.data['times'][i]) + '/')   
            
            try:
                com = str('cd ' + shot_dir + '&& mkdir ' + str(self.counter[i]))
                subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
            except:
                pass
            
            shot_dir = str(self.data['directory'] + str(self.data['shot number'])+ '/' + str(self.data['times'][i]) 
                            + '/' + str(self.counter[i]) +'/')    
            try:
                com = str('mv ' +  input_list[i][0] + ' ' + shot_dir) 
                subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
            except:
                print('Error occurred while moving input files')
                
            try:
                com = str('mv ' +  input_list[i][1] + ' ' + shot_dir) 
                subprocess.call(com, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
            except:
                print('Error occurred while moving input files')                
        
        return 
     
    
    def generate_input_files(self):
        
        self.check_for_files()
        
        if len(self.input_list)>0:
            print('\n'+'Starting input file generation' + '\n')
            master, sig_master = self.grab_data()
        
            print('\n' + 'Input files generated: ')
            
            for i in range(len(self.input_list)):
                self.data_to_vmec(master[i], self.input_list[i][0])
                self.data_to_v3fit(master[i], sig_master[i],
                                   self.input_list[i][0], self.input_list[i][1])
                
              

        
            self.create_dir_and_mv(self.input_list)
        
            print('\n' + 'Input files created and moved' + '\n')
            
        return 
    
    
    
    def file_and_dir_for_counter(self, count, time):
            new_vmec = str('input.' + str(self.data['shot number']) +'_' +
                           str(time)  + '_' + str(count) +'.vmec')


            new_v3fit = str('input.' + str(self.data['shot number']) +'_' +
                            str(time) +'_' + str(count) +'.v3fit')
            
            new_dir = str(self.data['directory'] + str(self.data['shot number'])+ '/' + str(time) 
                            + '/' + str(count) +'/')  
            
            return new_vmec, new_v3fit, new_dir
        
    
    def check_for_files(self):
        # This function serves to check for already existing input files so as 
        # to generate a new one with the correct counter
        # Files are named as input.shotnumber_time_counter.vmec(.v3fit)
        # Example: If input.14092626_1.6505_0.vmec exists then input.14092626_1.6505_1.vmec
        # will be made.
        
        #self.counter        = int(np.zeros(len(self.data['times'])))
        self.counter        = [int(0)]*len(self.data['times'])
        self.input_list     = [None]*len(self.counter)
        self.dir_list       = [None]*len(self.counter)
        self.made_list      = []
        
        for i in range(len(self.counter)):
            new_vmec, new_v3fit, new_dir = self.file_and_dir_for_counter(self.counter[i], 
                                                                         self.data['times'][i])       
            new_v3fit_dir = str(new_dir + new_v3fit)
            
            while os.path.exists(new_v3fit_dir):
                self.made_list.append([new_vmec, new_v3fit])
                self.counter[i] += 1
                new_vmec, new_v3fit, new_dir = self.file_and_dir_for_counter(self.counter[i], 
                                                                         self.data['times'][i]) 
                new_v3fit_dir = str(new_dir + new_v3fit)
                
            
            self.input_list[i]      = [new_vmec, new_v3fit]
            self.dir_list[i]        = new_dir
        
            
        if len(self.made_list)>0:
            print('\n'+'These input files already existed:')
            
            for i in range(len(self.made_list)):
                print('> ' + str(self.made_list[i][0]))
                print('> ' + str(self.made_list[i][1]))        
        

        self.data['directory_list'] = self.dir_list
        return 
    

    def read_result_parameters(self, result_file):
        f = Dataset(result_file)
        
        ns_steps    = f.variables['nsteps'][:]
        param_name  = self.decode_nc_string(f.variables['param_name'][:])
        param_index = f.variables['param_index'][:]
        param_value = f.variables['param_value'][:][ns_steps]

        return param_name, param_index, param_value
        
    
    def get_result_list(self):
        result_list = []
        for i in range(len(self.input_list)):
            result = str('result.' + self.input_list[i][1] + '.nc')
            result_list.append(result)
         
        self.result_list = result_list    
        return
    
    
    def edit_input(self, vmec_input_file, v3fit_input_file, result_file):
        param_name, param_index, param_value = self.read_result_parameters(result_file)
        
        #print(vmec_input_file)
        file = open(vmec_input_file, 'r')
        lines_vmec = file.readlines()
        file.close()
        
        #print(lines_vmec)
        

        for i, line in enumerate(lines_vmec):
            if line.startswith('PHIEDGE'):
                phi_ind = i
            elif line.startswith('AC'):
                ac_ind = i  
            elif line.startswith('AM'):
                am_ind = i  
            elif line.startswith('PRES_SCALE'):
                pres_ind = i  
        
        if param_value[21] > param_value[22]:
            param_value[21] = param_value[22]
        
        lines_vmec[phi_ind] = str('PHIEDGE = ' + str(param_value[0]) + ',\n')
        lines_vmec[ac_ind]  = str('AC = 1.0, ' + str(param_value[21]) +', ' +
                                  str(param_value[22]) + ',\n')
        lines_vmec[am_ind]  = str('AM = 1.0, ' + str(param_value[27]) +', 6.0,\n')        
        lines_vmec[pres_ind]= str('PRES_SCALE = ' + str(param_value[26])+',\n')


        os.remove(vmec_input_file)
        with open(vmec_input_file, 'w') as file:
            for line in lines_vmec:
                file.write(line)


        #print(v3fit_input_file)
        file2 = open(v3fit_input_file, 'r')
        lines_v3fit = file2.readlines()
        #print(lines_v3fit)
        file2.close()
         
        for i, line in enumerate(lines_v3fit):
            if line.startswith('pp_sxrem_af_a(1'):
                sxr_ind1 = i
            elif line.startswith('pp_sxrem_af_a(2'):
                sxr_ind2 = i            
            elif line.startswith('pp_ne_af'):
                ne_ind = i          
        

        lines_v3fit[sxr_ind1] = str('pp_sxrem_af_a(1,:) = ' + str(param_value[1]) + ', ' +
                                                              str(param_value[2]) + ', ' + 
                                                              str(param_value[3]) + ', ' +                                                              
                                                              str(param_value[4]) + ', ' +                                                              
                                                              str(param_value[5]) + ', ' +                                                              
                                                              str(param_value[6]) + ', ' +                                                              
                                                              str(param_value[7]) + ', ' +                                                              
                                                              str(param_value[8]) + ', ' +                                                              
                                                              str(param_value[9]) + ', ' +                                                              
                                                              str(param_value[10]) + ',\n')  
        
                                                              
        lines_v3fit[sxr_ind2] = str('pp_sxrem_af_a(2,:) = ' + str(param_value[11]) + ', ' +
                                                              str(param_value[12]) + ', ' + 
                                                              str(param_value[13]) + ', ' +                                                              
                                                              str(param_value[14]) + ', ' +                                                              
                                                              str(param_value[15]) + ', ' +                                                              
                                                              str(param_value[16]) + ', ' +                                                              
                                                              str(param_value[17]) + ', ' +                                                              
                                                              str(param_value[18]) + ', ' +                                                              
                                                              str(param_value[19]) + ', ' +                                                              
                                                              str(param_value[20]) + ',\n')   

        lines_v3fit[ne_ind] = str('pp_ne_af = ' + str(param_value[24]) + ', ' +
                                                    str(param_value[25]) + ', 0.0, 0.0,\n') 
                                                             
        os.remove(v3fit_input_file)
        with open(v3fit_input_file, 'w') as file:
            for line in lines_v3fit:
                file.write(line)  


        return

                                                       
    def generate_and_run(self):
        self.generate_input_files()
        
        try:
            for i in range(len(self.input_list)):
                print('\n')
                print('Reconstruction Started')
                com = str('cd ' + self.data['directory_list'][i] + ' && ' + self.v3_exe + ' ' + self.input_list[i][1] + ' -para=20')
                print('\n')
                subprocess.call(com, shell=True)
                
            print('Reconstructions completed')                
        except:
            print('Error: Reconstructions stopped')

        
        return

    def generate_and_run_vmec(self):
        self.generate_input_files()
        
        try:
            for i in range(len(self.input_list)):
                print('\n')
                print('Reconstruction Started')
                com = str('cd ' + self.data['directory_list'][i] + ' && ' + 'xvmec ' + self.input_list[i][0])
                print('\n')
                subprocess.call(com, shell=True)
                
            print('Reconstructions completed')                
        except:
            print('Error: Reconstructions stopped')

        
        return
    
    def generate_and_run_fastest(self, reverse_order=False):
        self.generate_input_files()
        self.get_result_list()
        
        #print(self.dir_list)
        if reverse_order:
            self.input_list.reverse()
            self.dir_list.reverse()
            self.result_list.reverse()
        
        
        try:
            i = 0
            for i in range(0, len(self.input_list)-1):
                print('\n')
                print('Reconstruction Started')
                com = str('cd ' + self.dir_list[i] + ' && ' + self.v3_exe + ' ' + self.input_list[i][1] + ' -para=20' )
                print('\n')
                subprocess.call(com, shell=True)

                current_output   = str(self.dir_list[i] + self.result_list[i])
                next_input_vmec  = str(self.dir_list[i + 1] + self.input_list[i + 1][0])
                next_input_v3fit = str(self.dir_list[i + 1] + self.input_list[i + 1][1])
                self.edit_input(next_input_vmec, next_input_v3fit, current_output)
                i += 1
            
            i = len(self.input_list) - 1
            print('\n')
            print('Reconstruction Started')

            com = str('cd ' + self.dir_list[i] + ' && ' + self.v3_exe + ' ' + self.input_list[i][1]  + ' -para=20')
            print('\n')
            subprocess.call(com, shell=True)            
                
                
            print('Reconstructions completed')                
        except:
            print('Error: Reconstructions stopped')

        
        return
    
    

    
        
    def print_input_names(self):
        try:
            print(self.input_list)
        except:
            print('You must generate input files first')
        












