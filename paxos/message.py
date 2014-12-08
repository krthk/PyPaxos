#!/usr/bin/python

from ballot import Ballot

class Message():
    PROPOSER_PREPARE    = 1
    ACCEPTOR_PROMISE    = 2
    ACCEPTOR_NACK       = 3
    
    PROPOSER_ACCEPT     = 4
    ACCEPTOR_ACCEPT     = 5
    
    PROPOSER_DECIDE     = 6
    
    LOG_SYNC_REQUEST    = 7
    LOG_SYNC_RESPONSE   = 8
        
    def __init__(self, round, messageType, source, ballot = None, metadata = None):
        self.source = source
        self.round = round
        self.ballot = ballot
        self.messageType = messageType
        self.metadata = metadata
    
    def __str__(self):
        return ('From:     {0}\n'
                'Round:    {1}\n' 
                'Ballot:   {2}\n'
                'Type:     {3}\n'
                'Metadata: {4}'.format(self.source, 
                                        self.round, 
                                        self.ballot, 
                                        self.messageType, 
                                        self.metadata))
                        