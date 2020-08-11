# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:41:39 2020

@author: hartwgj
"""

import multiprocessing as mp
import os
from datetime import datetime
import time


def worker(num):
    print('worker',num)
    time.sleep(5)
    print(datetime.now())
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

print('not in main')
if __name__ == '__main__':
    print('there are %s cores' %mp.cpu_count())
    jobs=[]
    for i in range(2):
        print('start job',i)
        p = mp.Process(target=worker,args=(i,))
        jobs.append(p)
    
    for j in jobs:
        j.start()
   
    for j in jobs:
        j.join()
        
    print("finished")
