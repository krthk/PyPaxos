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
        self.server = None
        self.threads = []
        
        self.isRunning = True
    
    
    #Networking setup
    def listen(self):
        self.open_socket()
        
        while True:
            if self.isRunning:
                #Establish connection with client
                client, addr = self.server.accept()
            
                #Dispatch thread to handle client
                threading.Thread(target=self.clientHandler, args=[client, addr])
            


    #Handle opening server socket
    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.bind((self.host,self.port))
        
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            
            print "Could not open socket: " + message
            sys.exit(1)

        while True:
            data, addr = sock.recvfrom(self.bufferSize)
            print "received message:", data


    #Threaded handler for clients
    def clientHandler(self, client, addr):
        print "Got connection from" + addr
        
        while True:
            if self.isRunning:
                data = client.recv(self.size)
                
                if not data:
                    break

                client.send(data)
    
            else:
                time.sleep(1)
        
        client.close()
    
    
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






