# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 12:59:04 2020

@author: hartwgj
"""

# cth 1mm interferometer code


import scipy.constants
from scipy import fft,ifft
from cthmds import CTHData
import numpy as np

# input the chord
# return the density and time axis
# other possible keywords: numfwin, phase,SAVEintfrm_1mm,eflag, verbose


#def CTHintfrm_1mm(shotnum,chord,debug):
def CTHintfrm_1mm(sawsig,intsig,chord,debug): # use when testing

# --------------------- Define constants ---------------------
    pi=scipy.constants.pi
    c = scipy.constants.c            # [m/s] speed of light, !const.c
    me = scipy.constants.m_e         # [kg] electron mass, !const.me
    ep0 = scipy.constants.epsilon_0  # [C^2/Nm^2] permitivity of free space, !const.eps0
    e = scipy.constants.e           # [C] fundamental charge, !const.e
   
    
# these are system dependent    
    freq=[244.0E9, 244.0E9, 244.0E9, 280.0E9] # chord frequencies
    w0 = 2.0*pi * np.array(freq)      # [Hz] nominal frequency of output
    lp = 2.0 * 0.25         #[m] closer to the flux surface width in ECRH plasmas
    dt=1.0/50E6             # 50MHz digitization rate
    sweepfreq=450000        # 450kHz sweep frequency
    hanning_width=70000     # window width of hanning window
    
    # for testing purposes
    shotnum=20032705
# define data board and channel pairs
#    sawtooth_ch=[(5,1),(6,2)] # one for each system
#    data_ch = [(5,2),(5,3),(5,4),(6,3)] # one for each channel    
    sawtooth_ch=[(5,1)] # one for each system
    data_ch = [(5,2)] # one for each channel
    

# ------------------------- Get data -------------------------

    # if debug: print('   Getting interferometer data...')
    
    intfrmraw=[]
    for board_channel in data_ch:
        intsig=CTHData('intgis')
        intsig.get_data(
            server='neil',
            shotnum=shotnum,
            board_channel=board_channel)
        intfrmraw.append(intsig.data)
    
    sawtoothraw=[]
    for board_channel in sawtooth_ch:
        sawsig=CTHData('intsaw')
        sawsig.get_data(
            server='neil',
            shotnum=shotnum,
            board_channel=sawtooth_ch[chord-1])
        sawtoothraw.append(sawsig.data)

    if debug:
        print('')
        print('   data retrieved, starting phase calculation... ')
        length=len(intsig.data)
        print('data length ',length)
        signal_strength=max(intsig.data[0:5000]) - min(intsig.data[0:5000])
        print('chord ',chord,'   signal strength ' ,signal_strength)

  
#   ; Truncate for efficiency 2^23=8388608 which should speed up calculations
#  that would go from 1.55s to 1.68 which is not long enough
# truncate=False
# if truncate:
#     numt=8288608
#     tstart=1.59
#     nstart=int((tstart-1.55)*50000000)
  
#     intfrm1 = intfrm1[nstart:nstart+numt-1]
#     intfrm2 = intfrm2[nstart:nstart+numt-1] 
#     intfrm3 = intfrm3[nstart:nstart+numt-1]
#     sawtooth = sawtooth[nstart:nstart+numt-1]
#     t_intfrm = t_intfrm[nstart:nstart+numt-1]


#  Compute fft of signals

    sawfft = np.fft.fft(sawsig.data)

    
    faxis=np.linspace(0.0,1.0/(2.0*dt),length//2)
    
    nfmax=int(sweepfreq/5.0)
    numfwin=int(hanning_width/5.0)
    
    abssawfft=np.abs(sawfft)
    maxsfft=np.max(abssawfft[1:length//2])
    
    nfmax = np.where(abssawfft==maxsfft)[0][0]
    if debug: print('nfmax = ',nfmax,' at f= ',faxis[nfmax])

# nfmax=90000
# ; numfwin sets the frequency window width used
# ; I'm not sure what the optimal value is, and it probably depends on the
# ; interferometer chirp frequency (i.e. sawtooth frequency)
    numfwin=hanning_width//5


# ; Apply frequency window.  Set usehanning = 1 to use a hanning window,
# ; otherwise a top hat window will be used
# usehanning=1
# if keyword_set(usehanning) then begin
#   hwin = hanning(2L*numfwin+1)
#   for ii=0,numchord-1 do begin
#     sigfft[nfmax-numfwin:nfmax+numfwin,ii] = hwin*sigfft[nfmax-numfwin:nfmax+numfwin,ii]
#   endfor
#   sigfft[0:nfmax-numfwin-1,*] = 0.0
#   sigfft[nfmax+numfwin+1:*,*] = 0.0
# endif else begin
#   ; Zero out all but frequencies within numfwin of nfmax
#   sigfft[0:nfmax-numfwin,*] = 0.0
#   sigfft[nfmax+numfwin:*,*] = 0.0
# endelse

# ; Do inverse transform for all chords
# sig = fft(sigfft,/inverse,dimension=1)

# ; Create cleaner reference signal from fft of sawtooth
# reffft = sawfft
# if keyword_set(usehanning) then begin
#   hwin = hanning(2L*numfwin+1)
#   reffft[nfmax-numfwin:nfmax+numfwin] = hwin*reffft[nfmax-numfwin:nfmax+numfwin]
#   reffft[0:nfmax-numfwin-1,*] = 0.0
#   reffft[nfmax+numfwin+1:*,*] = 0.0
# endif else begin
#   reffft[0:nfmax-numfwin] = 0.0
#   reffft[nfmax+numfwin:*] = 0.0
# endelse

# for ii=0,numchord-1 do begin
#   if ii eq 0 then ref = fft(reffft,/inverse) else $
#      ref = [[ref],[ref]]
# endfor

# ; Calculate phase difference between signals and reference
# phs = atan(sig*conj(ref),/phase)

# ; --------------------- Correct phase -------------------------
# phs = cthfringecounter(phs)

# ; Subtract offset and thin the data
# noffset = where( (t_intfrm ge 1.56) and (t_intfrm le 1.58) )
# for ii=0,numchord-1 do begin
#   if ii eq 0 then phase = thinn(phs[*,ii] - mean(phs[noffset,ii]),9) else $
#     phase = [[phase],[thinn(phs[*,ii] - mean(phs[noffset,ii]),9)]]
# endfor
# t_intfrm = thinn(t_intfrm,9)

# if n_elements(t_intfrm) ne n_elements(phase[*,0]) then $
#   message,'processed data and time axis not of same length!' 

# ; --------- Calculate density --------
# ;est_density = -(2.0 * !const.me * !const.eps0 * !const.c * w0 * phase) / (!const.e^2.0 * lp)
# est_density = -(2.0 * me * ep0 * c * w0 * phase) / (e^2.0 * lp)
# t0 = t_intfrm[0]
# tf = max(t_intfrm)
# ;dt = (tf - t0)/(numt - 1)
# taxis = t_intfrm
# dt = (tf - t0)/(n_elements(taxis)-1)

# if max(SAVEintfrm_1mm) eq 1 then begin
#   print,'   Saving data...'
#   for ii=0,numchord-1 do begin
#     if SAVEintfrm_1mm[ii] eq 1 then $
#       mdsput,'processed:intfrm_1mm:phs_'+strtrim(chord[ii],2), $
#       'BUILD_SIGNAL( $,*,build_range($,$,$))',phase[*,ii],t0,tf,dt
#   endfor
#   mdsput,'processed:intfrm_1mm:t0','$',t0
#   mdsput,'processed:intfrm_1mm:dt','$',dt
# endif

# if keyword_set(stp) then begin
#     print, 'cthintfrm_1mm.pro stopped for debugging at ', $
#       systime(0)
#     stop
# endif
# ; end of cthintfrm_1mm



