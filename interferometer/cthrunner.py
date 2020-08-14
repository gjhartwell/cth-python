# -*- coding: utf-8 -*-
"""

CTHrunner

mimics the cthrunday.idl program
looks for new shots and does stuff when it finds one.

Created on Mon Jul 20 14:27:00 2020

@author: hartwgj





"""

from cthmds import cthconnect
from cthmds import cthopen
import time
import datetime

def CTHrunner(**kwargs):
    
    if 'shotnum' not in kwargs:
        # create a first shotnum based on todays date
        date=datetime.datetime.now()
        shotnum=int(date.strftime('%y') \
                    +date.strftime('%m') \
                    +date.strftime('%d') \
                    +'01')
    else:
        shotnum=kwargs['shotnum']
        print(shotnum)
 
    CTHisrunning=True  
    while CTHisrunning:
        waitingfordata=True
        while waitingfordata:
            c=cthconnect(server='neil')
            cthopen(c,12345)
            prevnum=c.get('prevnum')
            
            if prevnum >= shotnum:
                waitingfordata=False
                print('processing shot',prevnum)
                shotnum=shotnum+1
            else:
                # pausing 5 seconds before next check
                time.sleep(5)
                continue
                



            
    