#!/usr/bin/python

import socket
import pickle
from message import Message
from paxos.ballot import Ballot


class PaxosRole:
    PROPOSER, LEARNER, ACCEPTOR = range(3)

class PaxosStage:
    SENT_PROPOSAL, SENT_PROMISE, SENT_ACCEPT = range(3)

class PaxosState(object):
    PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED = range(5)
    
    #Class "constructor"
    def __init__(self, port, otherServers):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.otherServers = otherServers
        
        self.round = 0
        self.role = None
        self.stage = None
        
        self.ballot = Ballot(self.ip, self.port)
    

    #Send to some server
    def send(self, message, ip, port):
        data = pickle.dumps(message)
        
        try:
            self.socket.sendto(data, (ip, port))
        
        except Exception as e:
            print e


    #Handle an incoming message
    def handleMessage(self, message):
        print "Received message with type:", message.messageType
    
        if message.messageType == Message.PROPOSE:
            print "0"

        elif message.messageType == Message.PREPARE:
            print "1"
    
        elif message.messageType == Message.PROMISE:
            print "2"

        elif message.messageType == Message.ACCEPT:
            print "3"

        elif message.messageType == Message.ACCEPTED:
            print "4"


    #Begin "Propose" phase
    def propose(self):
        self.role = PaxosRole.PROPOSER
        message = Message(Message.PROPOSE, self.ballot, self.round)
        
        for server in self.otherServers:
            self.send(message, server, self.port)

        self.stage = PaxosStage.SENT_PROPOSAL