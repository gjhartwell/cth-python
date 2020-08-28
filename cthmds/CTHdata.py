# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
#
#
# Parameters:
#	 
# Returns:
#
# Example:
#
# Also defines:
#
# Greg Hartwell
# 2017-11-27
# modified 2017-12-13 
#------------------------------------------------------------------

import numpy as np
from cthmds.cthconnect import cthconnect
from cthmds.tree_from_shot import tree_from_shot

#This CTHData class is more encompasing than the ReconCTHData
class CTHData(object):
    
# class members:
#   name - user defined name
#   data - numpy data array
#   taxis - numpy time axis
#   system_name - system specified name
#   formula - string holding formula information
#   unit - string holding unit value
#   gain -  the hardware gain
    
    def __init__(self,name):
        self.name=name
    
    def add_data(self,data):
        self.data=data
    
    def add_taxis(self,taxis):
        self.taxis=taxis
    
    def name(self):
        return self.name
    
    def data(self):
        return self.data
    
    def taxis(self):
        return self.taxis
    
    def system_name(self):
        return self.system_name
    
    def formala(self):
        return self.formula
    
    def unit(self):
        return self.unit
    
    def gain(self):
        return self.gain
    

    def get_data(self,**kwargs):
        # expecting server, shotnum, and one of tag, board_channel, channel
        # or node
        # server is passed to cthconnect, a wrapper for MDSplus connection
        # not all channels are tagged
        # board_channel is a board_channel pair
        # channel is a single channel number that needs to be devolved
        keywords_okay = keyword_tester(**kwargs)
        if keywords_okay:
            shotnum=kwargs['shotnum']
            
            # open a connection
            if 'server' in kwargs:
                server=kwargs['server']
            else:
                server=''
            mdsconn=cthconnect(server)
          
            # open shot
            tree=tree_from_shot(shotnum)
            mdsconn.openTree(tree,shotnum)
            
            # get data with appropriate method
            # Check that either a tag, 
            #                   a board/channel pair,
            #                   or a channel is given
            if 'tag' in kwargs:
                self.data=np.array(mdsconn.get(kwargs['tag']))
                timestring='dim_of('+kwargs['tag']+')'
                self.taxis=np.array(mdsconn.get(timestring))
            elif 'board_channel' in kwargs:
                board_channel=kwargs['board_channel']
                board=board_channel[0]
                channel=board_channel[1]
                # next actually get the data
                cthdata_board_channel(self,mdsconn,board,channel)
                
            elif 'node' in kwargs:
                self.data=np.array(mdsconn.get(kwargs['node']))
                timestring='dim_of('+kwargs['node']+')'
                self.taxis=np.array(mdsconn.get(timestring))
            
            elif 'channel' in kwargs:
                (board,channel)=channelToBoard(kwargs['channel'])
                #print("in CTHdata.getdata board channel = ", board,channel)
                #handles getting data, time axis, etc.
                cthdata_board_channel(self,mdsconn,board,channel)
            
            else:
                print('method not handled in cthdata.getdata')
            # close shot
            mdsconn.closeTree(tree,shotnum)
            
            # return
           
# 
# end of get_data method of CTHData class
#
            

#-----------------------------------------------------------------------------
#  Additional methods for CTHData class
#-----------------------------------------------------------------------------
    """
    Function to add a signal of same length to current signal.
    
    """
    def add_signal(self, signal_to_add):
        sigtype=type(signal_to_add)
        #print(sigtype.__name__)
        if sigtype.__name__ == 'CTHData':
            self.data=self.data+signal_to_add.data
        elif sigtype.__name__ == 'list':
            if len(list) == len(self.data):
                self.data=self.data+signal_to_add
            else:
                print("length of data not equal to length of signal_to_add")
        elif sigtype.__name__ == 'int':
            self.data = self.data + float(signal_to_add)
        elif sigtype.__name__ == 'float':
             self.data = self.data + float(signal_to_add)
        elif sigtype.__name__ == 'str':
             self.data = self.data + str(signal_to_add)
        else:
            print('add signal---type ',sigtype,' not supported')
    
    """
    Function to scale signal by scale_factor.
    """
    def multiply_signal(self, scale_factor):
        self.data = scale_factor * self.data
    
    """
    Function to zero a signal.
    """    
    def zero(self,**kwargs):
        # only kwarg allowed is length - length of data to average
        # for zeroing
        if 'length' not in kwargs:
            length = 1000
        ave_sig=sum(self.data[0:length])/float(length)
        self.data=self.data-ave_sig
            


#-----------------------------------------------------------------------------
# Converts the channel to the board, channel pair
def channelToBoard(channel):
    #print(channel)
    channel=int(channel)
    if channel <= 24:
        board=0
    else:
        channel -= 24
        board = int((channel-1) / 96) +1
        channel = (channel-1) % 96 +1 
    channel += 1
    return (board,channel)
#-----------------------------------------------------------------------------
# this is a private function that tests keywords in the get_data routine
# it just keeps the code more readable        
def keyword_tester(**kwargs):
    
    defined_keywords=['server','shotnum','tag','board_channel',
                      'channel','node']
    keywords_given=False
    
    # check that keywords are actually given
    if not len(kwargs):
        print("Error in keyword_tester - \
              No keywords given in call to get_data")
        print(defined_keywords)
        return None

    # make sure all keywords are legal
    for key in kwargs:
        if key not in defined_keywords:
            print("Error",key,"---Undefined Keyword in Call to get_data")
            print("Use: ",defined_keywords)
            return None
    
    # check that a shot number is given
    if 'shotnum' not in kwargs:
         print("Error in call to get_data --- no shot number given")
         return None
     
    # Check that either a tag, a board/channel pair, or a channel is given
    if 'tag' in kwargs:
        keywords_given=True
    elif 'board_channel' in kwargs:
        keywords_given=True
    elif 'channel' in kwargs:
        keywords_given=True
    elif 'node' in kwargs:
        keywords_given=True
    else:
        print("Error in call to get_data---\
              get_data needs either a tag, a board/channel pair,\
              a single channel number, or a node name")
        return 0
    
    return keywords_given
#-----------------------------------------------------------------------------
# end of keywords_given function
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# this function gets raw data from the MDSplus tree if the d-tacq board and
# channel number are given
# also handles storing    
def cthdata_board_channel(self,mdsconn,board,channel):

# String versions of board and channel, with a '0' in front of ch 1-9
    #print('board and channel = ',board,channel)
    brd_str = str(board)
    if channel <= 9:
        chn_str = '0' + str(channel)
    else:
        chn_str = str(channel)

# Construct the signal node name from board and channel
    if board == 0: # SCXI
        nodename = 'scxi:ch' + str(channel)
    elif board == 1: #D-TACQ 1
        nodename = 'acq196:input_' + chn_str
        gainname = 'acq1_com:ch' + chn_str + ':gain'
    elif board == 2: #D-TACQ 2
        nodename = 'acq1962:input_' + chn_str
        gainname = 'acq2_com:ch' + chn_str + ':gain'
    elif board == 3: #D-TACQ 3
        nodename = 'acq1963:input_' + chn_str
        gainname = 'acq3_com:ch' + chn_str + ':gain'
    elif board == 4: #D-TACQ 4
        nodename = 'acq1964:input_' + chn_str
        gainname = 'acq4_com:ch' + chn_str + ':gain'
    elif board == 5: # D-TACQ 5
        nodename = 'acqfast:input_'  + chn_str
        gainname = 'acqfast_com:ch' + chn_str + ':gain'
    elif board == 6: # D-TACQ 6
        nodename = 'acqfast2:input_' + chn_str
        gainname = 'acqfast2_com:ch' + chn_str + ':gain'
    elif board == 7: # D-TACQ 7
        nodename = 'acq1967:input_' + chn_str
        gainname = 'acq7_com:ch' + chn_str + ':gain'
    elif board == 8: # D-TACQ 8
        nodename = 'acq1968:input_' + chn_str
        gainname = 'acq8_com:ch' + chn_str + ':gain'
    else:
        print('Error in cthdata_board_channel ---\
              Improper board designation: ',board)
        data = 0
        return
# Get the gain
    if board == 0:
        gain = 1.0 # SCXI gain is 1.0
    else:
        try:
            gain = mdsconn.get(gainname)
        except:
            gain=1
        if (gain == 0) or (gain == None): 
            gain = 1.0
    self.gain=gain
# Get the data
    if mdsconn.get('$shot') >= 13091201:
        data = mdsconn.get(nodename) / self.gain 
        if len(data) <= 2:
            data = None
            return
    else:
    # Pre shot 13091201, the data had to be converted from bits to volts
    # Added condition so that print statement is not executed if messages 
    #are suppresed
    #if not keyword_set(quiet) then print,"error ",mdsconn.get('$shot')
    #commented out-MCAM
    #if board ge 9 then begin <---- WHO CHANGED THIS?
        print("cthdata_board_channel--shots prior to 13091201 not supported")
#        if board >= 6:
#            print('DTACQ ',brd_str,' not supported by cthdata.py prior to shot 13091201'
#  
#    # Get raw data in bits
#        data = mdsconn.get(nodename)
#        if (data == None) or (len(data) <= 2):
#            data = 0
#            return
#      
#    # Convert raw data to voltage for D-TACQ boards 1,2,3,4
#        if (board >= 1) and (board <= 4):
#            calminname = 'acq' + brd_str + '_com:calmin'
#            calmaxname = 'acq' + brd_str + '_com:calmax'
#            calmin = mdsconn.get(calminname)
#            calmax = mdsconn.get(calmaxname)
#        if (calmin == None) or (calmax == None):
#            calmin = -10.0
#            calmax =  10.0
#        else:
#            calmin = calmin[channel-1]
#            calmax = calmax[channel-1]
#        
#        data = ((calmax - calmin)*(data + 32768.0)/65535.0 + calmin) / gain
#    
#      
#    # Convert raw data to voltage for D-TACQ board 5
#        if board == 5:
#            data = data/3277.0# divide by bits per volt
    
#    Information about the signal node
# 

    if board == 0:
        signame = 'scxi:names:ch' + str(channel)
        formulaname = 'scxi:formula:ch' + str(channel)
    elif (board >= 1) and (board <= 4):
        signame = 'acq' + brd_str + '_com:ch' + chn_str + ':name'
        formulaname = 'acq' + brd_str + '_com:ch' + chn_str + ':formula'
    elif board == 5:
        signame = 'acqfast_com:ch' + chn_str + ':name'
        formulaname = 'acqfast_com:ch' + chn_str + ':formula'
    elif board == 6:
        signame = 'acqfast2_com:ch' + chn_str + ':name'
        formulaname = 'acqfast2_com:ch' + chn_str + ':formula'
    elif (board == 7) or (board == 8):
        signame = 'acq' + brd_str + '_com:ch' + chn_str + ':name'
        formulaname = 'acq' + brd_str + '_com:ch' + chn_str + ':formula'
    else:
        print('cthdata_board_formula---board ',board,' not supported')
    
    try:
        nameL = mdsconn.get(signame)
    except:
        nameL=''
    name = "".join(map(chr,nameL))
    
    try:
        formulaL = mdsconn.get(formulaname)
    except:
        formulaL=''
    formula = "".join(map(chr,formulaL))
    
    # parse the formula
    multiplier=1
    unit='arb'
    integrate=False
    if formula !='':
        if formula.find('i') >= 0:
            integrate=True
        if formula.find('*'):
            multiplier=float(formula[0:formula.find('*')])
        if formula.find('('):
            idx1=formula.find('(')+1
            idx2=formula.find(')')
            unit=formula[idx1:idx2]

    self.data=multiplier*np.array(data)
    self.integrate=integrate
    self.unit=unit
    self.formula=formula
    self.system_name=name
    
    if mdsconn.get('$shot') >= 13091201:
    # taxis is the same for all ch on a board, so just get taxis for ch 1
        if board == 0: # SCXI
            nodename = 'scxi:ch1'
        elif board == 1: #D-TACQ 1
            nodename = 'acq196:input_01'
        elif board == 2: #D-TACQ 2
            nodename = 'acq1962:input_01'
        elif board == 3: #D-TACQ 3
            nodename = 'acq1963:input_01'
        elif board == 4: #D-TACQ 4
            nodename = 'acq1964:input_01'
        elif board == 5: # D-TACQ 5
            nodename = 'acqfast:input_01'
        elif board == 6: # D-TACQ 6
            nodename = 'acqfast2:input_01'
        elif board == 7: # D-TACQ 7
            nodename = 'acq1967:input_01'
        elif board == 8: # D-TACQ 8
            nodename = 'acq1968:input_01'
        else:
            print('Error cthdata_board_channel---\
                  taxis area----Improper board designation: ',board)
            taxis = None
            return
        
        taxis = mdsconn.get('dim_of(' + nodename + ')')
        taxis = np.array(taxis)
        if len(taxis) <= 2:
            taxis = None 
        if board == 0:
            dt = 1.0 / float(mdsconn.get('scxi:time_base')) 
            taxis = dt*taxis
#  endif else begin
#    ;dt =  mdsvalue('slope_of(axis_of(dim_of(' + nodename + ')))',quiet=quiet)
#    nt = n_elements(taxis)
#    dt = (taxis[nt-1] - taxis[0]) / (nt-1)
#  endelse
    else:
        print(" in cthtaxis - shots greater than 13091201 not supported")
        taxis = None
    self.taxis=np.array(taxis)

#----------------------------------------------------------------------------
# end of cthdata_board_channel
#----------------------------------------------------------------------------