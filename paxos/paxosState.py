#!/usr/bin/python

import socket
import pickle
from sets import Set
from message import Message
from ballot import Ballot


class PaxosRole:
    PROPOSER    = 0
    ACCEPTOR    = 1
    LEARNER     = 2

class PaxosState(object):
    PROPOSER_SENT_PROPOSAL      = 0
    ACCEPTOR_SENT_PROMISE       = 1
    PROPOSER_SENT_ACCEPT        = 2
    ACCEPTOR_ACCEPTED           = 3
    PROPOSER_SENT_DECIDE        = 4
    ACCEPTOR_DECIDED            = 5
    LEARNER_DECIDED             = 6
    
    def __init__(self, round, role, stage, highestBallot = None, value = None):
        self.round = round
        self.role = role
        self.stage = stage
        self.highestBallot = highestBallot
        self.value = value
        self.responses = []

    def __str__(self):
        return ('Round:          {0}\n'
                'Role:           {1}\n' 
                'Stage:          {2}\n'
                'Highest Ballot: {3}\n'
                'Value:          {4}\n'
                'Responses:      {5}\n'.format(self.round, 
                                               self.role, 
                                               self.stage, 
                                               self.highestBallot,
                                               self.value, 
                                               self.responses))
                        