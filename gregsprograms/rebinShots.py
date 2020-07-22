# -*- coding: utf-8 -*-
"""
Created on Wed May 27 11:05:57 2020

@author: hartwgj
"""

# program to rebin shots in to months, quarters, years
# rebinShots(shots)
# counts number of shots in different periods

import matplotlib.pyplot as plt

def rebinShots(shots):
    
    
    period='month'

    monthArray=[int((shots[0]-(shots[0] % 10000))/10000)]
    narray=[0]
    idx=0
    for shot in shots:
         dshot=int((shot-(shot % 10000))/10000)
         if dshot == monthArray[idx]:
             narray[idx]=narray[idx]+1
         else:
             idx=idx+1
             monthArray.append(dshot)
             narray.append(0) 
             

    # check month array for missing months
    for idx in range(len(monthArray)):
        monthArray[idx]=monthArray[idx] % 100
    for idx in range(len(monthArray)-1):
        if (monthArray[idx+1]-monthArray[idx] == 1) or \
            (monthArray[idx+1]-monthArray[idx] == -11):
            continue
        else:
            monthArray.insert(idx+1,monthArray[idx]+1)
            narray.insert(idx+1,0)
    
    if period == 'month':
        #convert Month array to months
        months=['jan','feb','mar','apr','may','jun','jul','aug',\
                'sep','oct','nov','dec']
        strMonthArray=[]
        for idx in range(len(monthArray)):
            strMonthArray.append(months[monthArray[idx]-1])
            
        
        # print(strMonthArray)
        # print(narray)
               
        fig, ax=plt.subplots()
        ax.bar(strMonthArray,narray)
        ax.set_xlabel('month')
        ax.set_ylabel('number of OH shots')
        plt.show()
        
    elif period == 'quarter':
        quarters=['winter','spring','summer','fall']
        strQuarterArray=[]
        
        
       
 
        
        
        
        



    

