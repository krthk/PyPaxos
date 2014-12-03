#!/usr/bin/python

import socket
import threading
import pickle
from message import Message
from paxos.ballot import Ballot


class Round(threading.Thread):
    
    #Class "constructor"
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.localIP = ip
        self.localPort = port
        self.socket = None
        self.ballot = Ballot(self.localIP, self.localPort)
    
    
    #Called by starting the thread
    def run(self):
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