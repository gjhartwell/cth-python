# -*- coding: utf-8 -*-
"""

Capacitor Leakage Rate plots
Created on Tue Jul 14 10:43:53 2020

@author: hartwgj
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import datetime

df = pd.read_excel (r'C:\Users\hartwgj\Desktop\OH LV Capacitors\CapacitorLeakageCurrents.xlsx', \
                    usecols=[1])
#print (df)

lc=df.to_numpy()
length=len(lc)

print(lc)
print('capacitors tested = ', length)

matches=[x for x in lc if x<= 6.0]
good=len(matches)
print('good capaicitors = ',good)
print('percent good = ',100*good/length)

histbins=[1,2,3,4,5,6,7,8,9,10,11,12,20]
histbins=np.arange(1,6,1)

n,bins,patches=plt.hist(x=lc,bins=histbins,rwidth=0.85, \
                        alpha=0.7,color='blue')
histbins=np.arange(6,20,1)
n,bins,patches=plt.hist(x=lc,bins=histbins,rwidth=0.85, \
                        alpha=0.7,color='red')

plt.grid(axis='y')

x=datetime.datetime.now()
s='-- '+x.strftime("%b")+' '+x.strftime("%d")+' '+x.strftime("%Y")
plt.title('OH LV Leakage Currents '+s)
plt.xlabel('Leakage Current (mA)')
plt.ylabel('number of capacitors')

red_patch = mpatches.Patch(color='red', label='bad capacitors')
blue_patch = mpatches.Patch(color='blue', label='good capacitors')

plt.legend(handles=[blue_patch,red_patch])

s='total tested: '+str(length)
plt.annotate(s, (10,7.4))
s='percent good: {:4.1f}'.format(100*good/length)
plt.annotate(s, (10,6.5))



plt.show()
