#!/usr/bin/python

from ballot import Ballot

class Message():
    PROPOSER_PREPARE    = 1
    ACCEPTOR_PROMISE    = 2
    ACCEPTOR_NACK       = 3
    
    PROPOSER_ACCEPT     = 4
    ACCEPTOR_ACCEPT     = 5
    
    PROPOSER_DECIDE     = 6
    
        
    def __init__(self, round, messageType, source, ballot = None, value = None):
        self.round = round
        self.messageType = messageType
        self.source = source
        self.ballot = ballot
        self.value = value
    
    def __str__(self):
        return ('From:    {0}\n'
                'Round:   {1}\n' 
                'Ballot:  {2}\n'
                'Type:    {3}\n'
                'Value    {4}\n'.format(self.source, 
                                        self.round, 
                                        self.ballot, 
                                        self.messageType, 
                                        self.value))
                        