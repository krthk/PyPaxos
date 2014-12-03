#!/usr/bin/python

import socket
from message import MessageType
from message import Message


class Paxos(object):
    localProposalNum = 0
    localValue = 0
    
    #Class "constructor"
    def __init__(self):
        self.socket = None
        self.localProposalNum = 0
        self.localValue = 0
    
    
    #Networking setup
    def setup(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        except socket.error, (value, message):
            if self.socket:
                self.socket.close()
            
            print "Could not open socket: " + message
            sys.exit(1)


    #Send to some server
    def send(self, message, ip, port):
        if self.isRunning:
            data = pickle.dumps(message)
                self.socket.sendto(data, (ip, port))


    #Begin "Propose" phase
    def propose(self, messageType):
        ballot = Ballot()
        message = Message(MessageType.Propose, ballot)