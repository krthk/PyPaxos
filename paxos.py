#!/usr/bin/python

from message import MessageType
from message import Message


class Paxos(object):
    localProposalNum = 0
    localValue = 0
    
    #Class "constructor"
    def __init__(self):
        self.localProposalNum = 0
        self.localValue = 0


    #Begin "Propose" phase
    def propose(self, messageType):
        message = Message(MessageType.Propose, self.localProposalNum, self.localValue)
