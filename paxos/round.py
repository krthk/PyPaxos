#!/usr/bin/python

import socket
import threading
from message import MessageType
from message import Message


class Round(threading.Thread):
    
    #Class "constructor"
    def __init__(self):
        threading.Thread.__init__(self)
        self.localIP = ''
        self.localPort = 55555
        self.socket = None
        self.ballot = Ballot(self.localIP, self.localPort)
    
    
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
        message = Message(MessageType.Propose, self.ballot)
        
        #CHANGE THIS TO SEND TO NETWORK
        self.send(message, self.localIP, self.localPort)