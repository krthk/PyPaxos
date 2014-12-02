#!/usr/bin/python

import sys
import socket


class Node(object):
    
    #Class "constructor"
    def __init__(self):
        self.listenHost = ''
        self.listenPort = 55555
        self.bufferSize = 1024
        self.socket = None
        
        self.isRunning = True
    
    
    #Networking setup
    def setup(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.listenHost, self.listenPort))
        
        except socket.error, (value, message):
            if self.socket:
                self.socket.close()
            
            print "Could not open socket: " + message
            sys.exit(1)
        
        self.listen()


    #Listen to the network
    def listen(self):
        while True:
            if self.isRunning:
                data, addr = self.socket.recvfrom(self.bufferSize)
                print "Received data:", data

    
    #Send to some server
    def send(self, message, ip, port):
        if self.isRunning:
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






