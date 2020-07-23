# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:35:08 2018

@author: Greg
"""

#tcp tester
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "131.204.212.162"   
port = 2003               # Reserve a port for your service.
message='EOF'
s.connect((host, port))
print("connected")
s.send(message.encode('utf8'))
print("message sent")
back=s.recv(1024)
print("message recieved")
print(back.decode("utf8"))
s.close                     # Close the socket when done