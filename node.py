#!/usr/bin/python

import sys
import socket
import threading
import pickle
from paxos.paxosState import PaxosState


class Node(threading.Thread):
    
    #Class "constructor"
    def __init__(self):
        threading.Thread.__init__(self)
        self.localIP = ''
        self.localPort = 55555
        self.bufferSize = 1024
        self.socket = None
        self.isRunning = True
    
        self.currentRound = 0
        self.paxosRounds = {}
    
    
    #Called when thread is started
    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.localIP, self.localPort))
        
        except self.socket.error, (value, message):
            if self.socket:
                self.socket.close()
            
            print "Could not open socket: " + message
            sys.exit(1)

        self.localIP = socket.gethostbyname(socket.gethostname())
        print "\nRunning at: " + self.localIP + ":" + str(self.localPort)
        
        self.listen()


    #Listen to the network
    def listen(self):
        while True:
            if self.isRunning:
                data, addr = self.socket.recvfrom(self.bufferSize)
                
                if data:
                    try:
                        message = pickle.loads(data)

                        roundData = self.paxosRounds[message.round]
                        roundData.handleMessage(message)
                        
                
                    except Exception as e:
                        print e


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


    #Create a new paxos round
    def createPaxosRound(self):
        roundData = PaxosState(self.localIP, self.localPort)
        self.paxosRounds[self.currentRound] = roundData

        self.currentRound += 1






