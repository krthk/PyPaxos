#!/usr/bin/python

from ballot import Ballot

class Message(object):
    PROPOSE, PREPARE, PROMISE, ACCEPT, ACCEPTED = range(5)
    
    #Class "constructor"
    def __init__(self, messageType, ballot, round):
        self.messageType = messageType
        self.ballot = ballot
        self.round = round

