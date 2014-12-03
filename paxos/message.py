#!/usr/bin/python
class MessageType(Enum):
    PROPOSE, PROMISE, ACCEPT, ACCEPTED = range(4)


class Message(object):
    messageType = None
    proposalNumber = 0
    value = 0
    
    #Class "constructor"
    def __init__(self, messageType, proposalNumber, value):
        self.messageType = messageType
        self.proposalNumber = proposalNumber
        self.value = value

