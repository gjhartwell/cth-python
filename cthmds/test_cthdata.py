# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 08:48:38 2017

@author: Greg
"""

import matplotlib.pyplot as plt
from CTHdata import CTHData
from timeSubset import timeSubset

shot = 20092203
ibias=CTHData("iibas")
vbias=CTHData('vbias')
#mydata.get_data(shotnum=shot,tag='\\V_LOOP_AVG')
#mydata.get_data(shotnum=shot,node='processed:intfrm_1mm:int_nedl_1')
ibias.get_data(shotnum=shot,board_channel=(2,96))
vbias.get_data(shotnum=shot,board_channel=(2,95))
#mydata.get_data(shotnum=shot,channel=108)
# print(mydata.name)
# print(mydata.formula)
# print(mydata.unit)
# print(mydata.gain)
#print(mydata.system_name)
#mydata.multiply_signal(2)
#mydata2=mydata
#mydata.add_signal(10000)
#mydata.add_signal(mydata2)
#mydata.zero()

plt.plot(ibias.taxis,ibias.data)
plt.xlim(1.6,1.7)
plt.show()


plt.plot(vbias.taxis,vbias.data)
plt.xlim(1.6,1.7)

plt.show()

#getCTHData() 
#getCTHData(cthconn) 
#getCTHData(cthconn,bob=10092235)
#getCTHData(bob=10092235)
#getCTHData(tag="\\I_p")
#getCTHData(cthconn,tag="\\I_p")
#getCTHData(cthconn,channel=96)
#getCTHData(board_channel=[1,96])

#cthconn.closeTree(tree,shot)
#cthconn.close()