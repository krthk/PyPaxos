#!/usr/bin/python

import sys
import socket
import threading
import time
import Queue
import pickle
from paxos.messagepump import MessagePump
from paxos.paxosState import PaxosState


class Node(threading.Thread):
    
    #Class "constructor"
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.port = 55555
        
        self.otherServers = []
    
        self.currentRound = 0
        self.paxosRounds = {}
    
        self.queue = Queue.Queue()
        self.messagePump = MessagePump(None, self.port, self.queue)
    
    
    #Called when thread is started
    def run(self):
        #Get list of other servers
        self.otherServers = open("config").read().splitlines()
        
        self.messagePump.setDaemon(True)
        self.messagePump.start()
        
        while True:
            if not self.queue.empty():
                try:
                    data = self.queue.get()
                    print "RECV", data
                    message = pickle.loads(data)
                        
                    roundData = self.paxosRounds[message.round]
                    roundData.handleMessage(message)
                    
                except Exception as e:
                    print e
        
            time.sleep(5)


    #Stop all network activity
    def fail(self):
        if not self.messagePump.isRunning:
            print "Already failed"
        
        else:
            self.messagePump.isRunning = False
            print "Halting activity"


    #Resume network activity
    def unfail(self):
        if self.messagePump.isRunning:
            print "Already running"
        
        else:
            self.messagePump.isRunning = True
            print "Resuming activity"


    #Create a new paxos round
    def createPaxosRound(self):
        roundData = PaxosState(self.port, self.otherServers)
        self.paxosRounds[self.currentRound] = roundData

        self.currentRound += 1






