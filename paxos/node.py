#!/usr/bin/python

import sys
import socket
import threading
import time
import Queue
import pickle
import math
import random
from sets import Set
from messagepump import MessagePump
from paxosState import PaxosState
from paxosState import PaxosRole
from message import Message
from ballot import Ballot
from log import Log


class Node(threading.Thread):
    
    def __init__(self, ip, port = 55555):
        threading.Thread.__init__(self)
        
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Read config and add the servers to the set
        self.serverSet = Set()
        for server in open('../config').read().splitlines():
            _ip, _port = server.split(':')
            
            # Only add if it is not the local server
            if _ip != self.addr[0] or int(_port) != self.addr[1]:
                self.serverSet.add((_ip, int(_port)))
        
        self.numServers = len(self.serverSet)
        
        # Compute the size of the majority quorum
        # Must add 1 to numServers because the local server is not in that set
        self.quorumSize = int((self.numServers+1)/2)+1
        
        self.lastRound = -1
        self.paxosStates = {}
    
        self.queue = Queue.Queue()
        self.msgReceived = threading.Event()
        self.msgReceived.clear()
    
        self.messagePump = MessagePump(self.queue, self.msgReceived, owner = self, port = self.addr[1])
        self.messagePump.setDaemon(True)
    
        self.log = Log()
    
    
    # Called when thread is started
    def run(self):
        # Get list of other servers
        self.messagePump.start()
        
        while True:
            self.msgReceived.wait()
            while not self.queue.empty():
                data, addr = self.queue.get()
                print 'Received on ', self.addr
                try:
                    msg = pickle.loads(data)
                    print msg
                    self.processMessage(msg, addr)
                except Exception as e:
                    print data
                    print e
            self.msgReceived.clear()

    # Process the message msg received from the address addr
    def processMessage(self, msg, addr):
        # The round corresponding to the message
        r = msg.round

        # Check if it is a PROPOSE message
        if msg.messageType == Message.PROPOSER_PREPARE:
            # Check if we already have sent/received a message for this round 
            if r in self.paxosStates:
                # Get the state corresponding to the current round
                state = self.paxosStates[r]
                
                # Respond to the proposer with a promise not to accept any lower ballots
                if msg.ballot >= state.highestBallot:
                    promise_msg = Message(msg.round, 
                                          Message.ACCEPTOR_PROMISE, 
                                          self.addr,
                                          state.highestBallot, 
                                          state.value)
                    print '1Sending promise to', msg.source
                    self.sendMessage(promise_msg, msg.source)
                    
                    # Update the state corresponding to the current round
                    self.paxosStates[r] = PaxosState(r, PaxosRole.ACCEPTOR, 
                                                     PaxosState.ACCEPTOR_SENT_PROMISE, 
                                                     msg.ballot, 
                                                     msg.value)
                
                # Send a NACK message if we have already promised to a higher ballot
                else:
                    nack_msg = Message(msg.round, 
                                       Message.ACCEPTOR_NACK, 
                                       self.addr,
                                       state.highestBallot, 
                                       state.value)
            
            # We haven't touched this round yet. So, accept the proposal and send a promise 
            else:
                # Respond to the proposer with a promise not to accept any lower ballots
                promise_msg = Message(msg.round, 
                                      Message.ACCEPTOR_PROMISE,
                                      self.addr)
                print '2Sending promise to', msg.source
                self.sendMessage(promise_msg, msg.source)
                
                # Update the state corresponding to the current round
                self.paxosStates[r] = PaxosState(r, PaxosRole.ACCEPTOR, 
                                                 PaxosState.ACCEPTOR_SENT_PROMISE,  
                                                 msg.ballot, 
                                                 msg.value)

        elif msg.messageType == Message.ACCEPTOR_PROMISE:
            # Ensure we are the proposer for this round 
            if r not in self.paxosStates: return  
            if self.paxosStates[r].role != PaxosRole.PROPOSER: return

            # This is a valid promise from one of the servers
            # Add this server to the set of positive responses 
            self.paxosStates[r].responses.add((msg.source, msg.ballot, msg.value))
            
            # Check if we have a quorum
            if len(self.paxosStates[r].responses) >= self.quorumSize:
                # Add code to check the last value and send a accept
                # to majority of servers
                pass
        
        elif msg.messageType == Message.ACCEPTOR_NACK:
            # If we receive a NACK message from any of the servers, abandon this round
            # because we are never going to succeed with the current ballot number
            
            # Add code to implement the above
            pass
                
        elif msg.messageType == Message.PROPOSER_ACCEPT:
            pass

    # Returns a list of servers that create a quorum
    def getQuorum(self):
        return random.sample(self.serverSet, self.quorumSize)
    
    # Serialize and send the given message msg to the given address addr
    def sendMessage(self, msg, addr):
        print self.addr, 'sent message to', addr
        data = pickle.dumps(msg)
        self.socket.sendto(data, addr)
    
    # Stop all network activity
    def fail(self):
        if not self.messagePump.isRunning:
            print "Already failed"
        
        else:
            self.messagePump.isRunning = False
            print "Halting activity"

    # Resume network activity
    def unfail(self):
        if self.messagePump.isRunning:
            print "Already running"
        
        else:
            self.messagePump.isRunning = True
            print "Resuming activity"


if __name__ == '__main__':
    n = Node('127.0.0.1', 55555)
    n.start()

    n2 = Node('127.0.0.1', 55556)
    n2.start()
    
    time.sleep(2)
    b = Ballot('127.0.0.1', 55556)
    msg = Message(0, Message.PROPOSER_PREPARE, n2.addr, b)
    n2.sendMessage(msg, ('127.0.0.1', 55555))
    time.sleep(2)
    
    print n.paxosStates[0]
    print n2.paxosStates

    n3 = Node('127.0.0.1', 55557)
    n3.start()
    time.sleep(2)
    b2 = Ballot('127.0.0.1', 55557)
    msg = Message(0, Message.PROPOSER_PREPARE, n3.addr, b2)
    n3.sendMessage(msg, ('127.0.0.1', 55555))
    time.sleep(2)
    print n.paxosStates[0]

#     time.sleep(3)
#     b.increment()
#     msg = Message(0, Message.ACCEPTOR_ACCEPT, n2.addr, b)
#     n2.sendMessage(msg, ('127.0.0.1', 55555))
    
#     prep_msg = Message(0, Message.PROPOSER_PREPARE, n2.addr, b, None)
#     n2.sendMessage(prep_msg, ('127.0.0.1', 55555))


