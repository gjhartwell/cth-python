# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:32:37 2020

@author: hartwgj
"""

def getusestate(shotnum)
  # ;+
  # ; :Description:
  # ;    Gets the USESTATE for a shot, where.
  # ;
  # ;    bit 1 - SCXI
  # ;    bit 2 - MGs
  # ;    bit 3 - dtacq1
  # ;    bit 4 - ECRH
  # ;    bit 5 - OH
  # ;    bit 6 - Interlock
  # ;    bit 7 - Cooling
  # ;    bit 8 - Vacuum
  # ;    bit 9 - dtacq2
  # ;    bit 10 - Gas Puffer
  # ;    bit 11 - Integrate
  # ;    bit 12 - TrigA
  # ;    bit 13 - HF SCR
  # ;    bit 14 - TVF SCR
  # ;    bit 15 - RF reset
  # ;    bit 16 - Radial Field
  # ;    bit 17 - Trig B
  # ;    bit 18 - Trig C
  # ;    bit 19 - dtacq3
  # ;    bit 20 - dtacq4
  # ;    bit 21 - dtacq5
  # ;    bit 22 - paddle
  # ;    bit 1 - SCXI
  # ;    bit 1 - SCXI
  # ;
  # ; :Keywords:
  # ;    shotnum
  # ;
  # ; :Examples:
  # ;
  # ; :Author: Greg
  # ; :History: modified for python - May 26,2020
  # ;-

import cthmds

    c=cthmds.cthconnect("mds")
    cthmds.cthopen(c,shotnum)
  
    usestate=c.get('usestate')
    usestate = [int(i) for i in list('{0:0b}'.format(usestate))] 
    usestate.reverse()
    
  return,usestate

end
