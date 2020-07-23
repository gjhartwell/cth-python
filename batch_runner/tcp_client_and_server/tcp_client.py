# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 08:26:21 2018

@author: Greg
"""

# tcp_client example from https://pymotw.com/2/socket/tcp.html

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening

def tcp_client(message):
    server_address = ('131.204.212.162', 2003)
    print ('connecting to %s port %s' % server_address)
    sock.connect(server_address)
    
    try:
        # Send data
        #message = 'This is the message.  It will be repeated.'
        print('sending "%s"' % message)
        sock.sendall(message.encode('utf8'))
    
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        datan=''
        while amount_received < amount_expected:
            data_bytes = sock.recv(16)
            data=data_bytes.decode('utf8')
            datan=datan+data
            amount_received += len(data)
            print ('received "%s"' % data)
    
    finally:
        print ('closing socket')
        print(datan)
        sock.close()

#testing
tcp_client("9File Type144vmec11Shot Number31409223510Time Slice61.614DATA183EOF")
