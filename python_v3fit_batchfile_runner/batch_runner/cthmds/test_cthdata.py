# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 08:48:38 2017

@author: Greg
"""

import matplotlib.pyplot as plt
from CTHdata import CTHData
from timeSubset import timeSubset

shot = 20032705
mydata=CTHData("atest")
#mydata.get_data(shotnum=shot,tag='\\I_p')
mydata.get_data(shotnum=shot,node='processed:intfrm_1mm:int_nedl_1')
#mydata.get_data(shotnum=shot,board_channel=(1,96))
#mydata.get_data(shotnum=shot,channel=96)
print(mydata.name)
print(mydata.formula)
print(mydata.unit)
print(mydata.gain)
print(mydata.system_name)
#mydata.multiply_signal(2)
#mydata2=mydata
#mydata.add_signal(10000)
#mydata.add_signal(mydata2)
#mydata.zero()
taxis=timeSubset(mydata.taxis,mydata.taxis,1.6,2.0)
data=timeSubset(mydata.taxis,mydata.data,1.6,2.0)
plt.plot(taxis,data)
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