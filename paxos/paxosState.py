#!/usr/bin/python

import socket
import pickle
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
    PROPOSER_SENT_DECIDE        = 3
    ACCEPTOR_DECIDED            = 4
    LEARNER_DECIDED             = 5
    
    def __init__(self, round, role, stage, highestBallot = None, value = None):
        self.round = round
        self.role = role
        self.stage = stage
        self.highestBallot = highestBallot
        self.value = value
        self.responses = None