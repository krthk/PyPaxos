#!/usr/bin/python

import socket
import pickle
from message import Message
from paxos.ballot import Ballot


class PaxosRole:
    SENT_PROPOSAL, LEARNER, ACCEPTOR = range(3)

class PaxosStage:
    PROPOSER, LEARNER, ACCEPTOR = range(3)

class PaxosState(object):
    PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED = range(5)
    
    #Class "constructor"
    def __init__(self, ip, port):
        self.localIP = ip
        self.localPort = port
        self.socket = None
        
        self.role = None
        self.stage = None
        
        self.ballot = Ballot(self.localIP, self.localPort)
    
        self.setup()
    
    
    #Socket setup
    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.propose()
    

    #Send to some server
    def send(self, message, ip, port):
        data = pickle.dumps(message)
        self.socket.sendto(data, (ip, port))


    #Begin "Propose" phase
    def propose(self):
        message = Message(Message.PROPOSE, self.ballot)
        
        #CHANGE THIS TO SEND TO NETWORK
        self.send(message, self.localIP, self.localPort)