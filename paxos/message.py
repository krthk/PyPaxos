#!/usr/bin/python

from ballot import Ballot

class MessageType(Enum):
    PROPOSE, PROMISE, ACCEPT, ACCEPTED = range(4)


class Message(object):
    
    #Class "constructor"
    def __init__(self, messageType, ballot):
        self.messageType = messageType
        self.ballot = ballot

