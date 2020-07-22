# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 11:09:23 2017

@author: James Kring  
@email:  jdk0026@auburn.edu                   
"""
# =============================================================================
# Purpose: Grab data from CTH Tree
# 
# To Do: 
# =============================================================================

# =============================================================================
# shot = 15102408
# 
# infrm = CTHData(shot, 'processed:intfrm_1mm:int_nedl_1')
# 
# plt.figure()
# plt.plot(infrm.time, infrm.data)
# =============================================================================

from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import MDSplus as mds
import numpy as np
import numexpr as ne
from scipy.signal import savgol_filter
#from v3fit_util import disrupt_time

def find_closest_index(array, value):
    new_array = abs(np.array(array) - value)
    
    try:
        index = new_array.argmin()
    except:
        print('Invalid Array')
        index = 0
        
        
    return int(index)



class CTHData:
    
    def __init__(self, shot, data_channel, channel_number=False, **kwargs):
        self.name = None
        self.gain = None
        self.formula = None        
        self.shot = shot
        self.data_channel = data_channel
        self.channel_number = channel_number
        self.get_channel()
        self.time, self.data= self.get_raw_data()

        
    def get_raw_data(self):
        tree = 't' + str(self.shot)[0:6]
                
        conn = mds.connection.Connection('mds.physics.auburn.edu')
        #conn = mds.connection.Connection('131.204.212.37')
        conn.openTree(tree, self.shot)

        data        = np.array(conn.get(self.data_channel).data()).astype(np.float)
        time        = np.array(conn.get(str('dim_of('+self.data_channel + ')'))).astype(np.float)
        

        try:
            gain    = conn.get(self.gain_channel).data()
        except:
            gain    = 1

        try:
            name =  bytearray(conn.get(self.name_channel).data().tolist()).decode("utf-8")
        except:
            name = False
            
            
        self.name = name
        self.gain = gain
        if self.channel_number:
            try:
                if self.board == 0:
                    form_channel = str('scxi:formula:ch' + str(self.channel))
                    formula = bytearray(conn.get(form_channel).data().tolist()).decode()

                    formula = formula.split("(")[0]
                    
                    #data = self.scale_and_offset(data, self.board, self.channel)
                    data = data/gain
                    
                    x = data
                    data = ne.evaluate(formula)
                    #data = zero_beginning(data)
                    #dt = 1.0 / float(conn.get('scxi:time_base')) 
                    #time = dt*time


                else:
                    form_channel = str('acq' + str(self.board) + '_com:ch' + str(self.channel).zfill(2) + ':formula')
                    #print(form_channel)
                    formula = bytearray(conn.get(form_channel).data().tolist()).decode()                
                    #print(formula)
                    formula = formula.split("(")[0]

                    #ata = self.scale_and_offset(data, self.board, self.channel)
                    #print(formula)
                    #print(gain)
                    data = data/gain
                    x = data
                    data = ne.evaluate(formula)
                    
                    #data = zero_beginning(data)
                    
                self.formula = formula    
            except:
                #print('Formula not found')
                self.formula=None
                data = data/gain
                pass
        else:
            data = data / gain
            
        #print(str(self.data_channel) + ': ' + str(time[0]) + '    ' + str(time[-1]))   
        return  time, data


    def get_channel(self):
        if self.channel_number:
            board, channel = self.number_to_board_channel(self.data_channel)
            self.data_channel, self.gain_channel, self.name_channel =  self.board_channel_to_node(board, channel)
            self.board, self.channel = board, channel

        else:
            self.data_channel = self.data_channel
            self.gain_channel = str(self.data_channel + ':gain')
            self.name_channel = str(self.data_channel + ':name')   
            
            
        
        return
            
        
    def number_to_board_channel(self, channel):
        channel = int(channel)
        if channel <= 24:
            board = 0
        else:
            channel -= 24
            board = int((channel)/96) + 1
            channel = (channel) % 96
        channel += 1 
        #print(board, channel)
        return board, channel
    
    
    def board_channel_to_node(self, board, channel):
        #brd_str = str(board)
        if channel <= 9:
            chn_str = '0' + str(channel)
        else:
            chn_str = str(channel)
        
        if board == 0: # SCXI
            nodename = 'scxi:ch' + str(channel)
            gainname = ''
            namename = ''
        elif board == 1: #D-TACQ 1
            nodename = 'acq196:input_' + chn_str
            gainname = 'acq1_com:ch' + chn_str + ':gain'
            namename = 'acq1_com:ch' + chn_str + ':name'
        elif board == 2: #D-TACQ 2
            nodename = 'acq1962:input_' + chn_str
            gainname = 'acq2_com:ch' + chn_str + ':gain'
            namename = 'acq2_com:ch' + chn_str + ':name'
        elif board == 3: #D-TACQ 3
            nodename = 'acq1963:input_' + chn_str
            gainname = 'acq3_com:ch' + chn_str + ':gain'
            namename = 'acq3_com:ch' + chn_str + ':name'            
        elif board == 4: #D-TACQ 4
            nodename = 'acq1964:input_' + chn_str
            gainname = 'acq4_com:ch' + chn_str + ':gain'
            namename = 'acq4_com:ch' + chn_str + ':name'            
        elif board == 5: # D-TACQ 5
            nodename = 'acqfast:input_'  + chn_str
            gainname = 'acqfast_com:ch' + chn_str + ':gain'
            namename = 'acqfast_com:ch' + chn_str + ':name'            
        elif board == 6: # D-TACQ 6
            nodename = 'acqfast2:input_' + chn_str
            gainname = 'acqfast2_com:ch' + chn_str + ':gain'
            namename = 'acqfast2_com:ch' + chn_str + ':name'            
        elif board == 7: # D-TACQ 7
            nodename = 'acq1967:input_' + chn_str
            gainname = 'acq7_com:ch' + chn_str + ':gain'
            namename = 'acq7_com:ch' + chn_str + ':name'            
        elif board == 8: # D-TACQ 8
            nodename = 'acq1968:input_' + chn_str
            gainname = 'acq8_com:ch' + chn_str + ':gain'
            namename = 'acq8_com:ch' + chn_str + ':name'            
        else:
            print('Error in cthdata_board_channel ---\
                  Improper board designation: ',board)  
 
        return nodename, gainname, namename
            
    """
    Function to add a signal of same length to current signal.
    """
    def add_signal(self, signal_to_add):
        new_signal = self.data + signal_to_add
        return new_signal
    
    
    """
    Function to scale signal by scale_factor.
    """
    def multiply_signal(self, scale_factor):
        new_signal = scale_factor * self.data
        return new_signal


#ip   = CTHData(14092626, '\I_P')

#plt.plot(ip.time, ip.data)


# =============================================================================
# #sxr = CTHData(20020519,'processed:sxr:sxrdeconsigs:sd252000tn10')

#print(sxr.time)
# test = CTHData(18101242, '119', channel_number=True)
#ip   = CTHData(20012843, '\I_P')
# print(test.data_channel)
# print(test.gain)
#plt.plot(ip.time, ip.data)
# #plt.xlim([1.6, 1.7])
# print('Done')
# 
# =============================================================================

#ip   = CTHData(20021052, 171,channel_number=True)
#PI096A = CTHData(20021052, 180, channel_number=True)

#print(PI096A.time[0], ip.time[0])


#plt.figure()
#plt.plot(PI096A.time, PI096A.data, 'k')
#plt.plot(ip.time, ip.data ,'r')
#plt.xlim([1.62, 1.64])
