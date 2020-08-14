# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 14:34:20 2018

@author: Greg
"""
import tkinter as tk

def callErrorDialog(error):
    
    master = tk.Tk()
    msg=tk.Message(master,text=error)
    msg.config(bg='lightblue',font=("times",24))
    msg.pack
    tk.wait_window()

 
error="This is just a  test error"   
callErrorDialog(error)   