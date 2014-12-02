#!/usr/bin/python

import sys
import socket
import threading
import time


class Server(object):
    
    #Class "constructor"
    def __init__(self):
        self.host = ''
        self.port = 55555
        self.bufferSize = 1024
        self.socket = None
        
        self.isRunning = True
    
    
    #Networking setup
    def listen(self, port):
        self.port = port
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.host, self.port))
        
        except socket.error, (value, message):
            if self.socket:
                self.socket.close()
            
            print "Could not open socket: " + message
            sys.exit(1)

        while True:
            data, addr = self.socket.recvfrom(self.bufferSize)
            
            if self.isRunning:
                print "Received data:", data


    #Send to some server
    def send(self, message, ip, port):
        self.socket.sendto(message, (ip, port))
    
    #Stop all network activity
    def fail(self):
        if not self.isRunning:
            print "Already failed"
        
        else:
            self.isRunning = False
            print "Halting activity"


    #Resume network activity
    def unfail(self):
        if self.isRunning:
            print "Already running"
        
        else:
            self.isRunning = True
            print "Resuming activity"






