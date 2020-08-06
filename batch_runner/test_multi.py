# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 14:41:39 2020

@author: hartwgj
"""

import multiprocessing as mp
import os

print('there are %s cores' %mp.cpu_count())
def worker(num):
    print('worker',num)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

if __name__ == '__main__':
    for i in range(2):
        print('start job',i)
        p = mp.Process(target=worker,args=(i,))
        p.start()
        p.join()
