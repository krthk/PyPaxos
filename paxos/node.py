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


class Node(threading.Thread):
    
    def __init__(self, ip, port = 55555):
        threading.Thread.__init__(self)
        
        self.addr = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Read config and add the servers to the set
        self.serverSet = Set()
        for server in open('config2').read().splitlines():
            _ip, _port = server.split(':')
            
            # Only add if it is not the local server
            if _ip != self.addr[0] or int(_port) != self.addr[1]:
                self.serverSet.add((_ip, int(_port)))
        
        # Number of servers in the system including self
        self.numServers = len(self.serverSet) + 1
        
        # Compute the size of the majority quorum
        self.quorumSize = int(self.numServers/2)+1
        
        self.lastRound = -1
        self.paxosStates = {}
    
        self.queue = Queue.Queue()
        self.msgReceived = threading.Event()
        self.msgReceived.clear()
    
        self.messagePump = MessagePump(self.queue, self.msgReceived, owner = self, port = self.addr[1])
        self.messagePump.setDaemon(True)
    
    # Called when thread is started
    def run(self):
        # Get list of other servers
        self.messagePump.start()
        
        while True:
            self.msgReceived.wait()
            while not self.queue.empty():
                data, addr = self.queue.get()
                try:
                    msg = pickle.loads(data)
                    print '{0}: Received\n{1}'.format(self.addr, msg)
                    self.processMessage(msg, addr)
                except Exception as e:
                    print '{0}: {1}'.format(self.addr, data)
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
                                          msg.ballot, 
                                          {'highestballot': state.highestBallot, 'value': state.value})
                    print '{0}: Sending promise to {1}'.format(self.addr, msg.source)
                    self.sendMessage(promise_msg, msg.source)
                    
                    # Update the state corresponding to the current round
                    self.paxosStates[r] = PaxosState(r, PaxosRole.ACCEPTOR, 
                                                     PaxosState.ACCEPTOR_SENT_PROMISE, 
                                                     msg.ballot,
                                                     state.value)
                
                # Send a NACK message if we have already promised to a higher ballot
                else:
                    nack_msg = Message(msg.round, 
                                       Message.ACCEPTOR_NACK, 
                                       self.addr,
                                       msg.ballot, 
                                       {'highestballot': state.highestBallot, 'value': state.value})
                    print '{0}: Sending a NACK to {1}'.format(self.addr, msg.source)
                    self.sendMessage(nack_msg, msg.source)
            
            # We haven't touched this round yet. So, accept the proposal and send a promise 
            else:
                # Respond to the proposer with a promise not to accept any lower ballots
                promise_msg = Message(msg.round, 
                                      Message.ACCEPTOR_PROMISE,
                                      self.addr, 
                                      msg.ballot,
                                      {'highestballot': None, 'value': None})
                print '{0}: Sending promise to {1}'.format(self.addr, msg.source)
                self.sendMessage(promise_msg, msg.source)
                
                # Update the state corresponding to the current round
                self.paxosStates[r] = PaxosState(r, PaxosRole.ACCEPTOR, 
                                                 PaxosState.ACCEPTOR_SENT_PROMISE,  
                                                 msg.ballot)

        elif msg.messageType == Message.ACCEPTOR_PROMISE:
            print '{0}: Received a promise from {1}'.format(self.addr, msg.source)
            # Ensure we are the proposer for this round 
            if r not in self.paxosStates: return
            
            # Get the state corresponding to the current round
            state = self.paxosStates[r]

            # Return if I am not a proposer
            if state.role != PaxosRole.PROPOSER: return
            # Return if the PROMISE response is not for my current highest ballot
            if state.highestBallot != msg.ballot: return 
            
            # This is a valid promise from one of the servers
            # Add this server to the set of positive responses 
            state.responses.append((msg.source, msg.metadata['highestballot'], msg.metadata['value']))
            
            # Check if we have a quorum. +1 to include ourself
            if len(state.responses) + 1 >= self.quorumSize:
                # Get the value corresponding to the highest ballot
                highestBallot, highestValue = None, None
                for (_, ballot, value) in state.responses:
                    if highestBallot == None:
                        highestBallot, highestValue = ballot, value
                    elif ballot > highestBallot:
                        highestBallot, highestValue = ballot, value
                
                print '{0}: PROMISE Quorum formed'.format(self.addr)
                print '{0}: Sending ACCEPT messages to all ACCEPTORS'.format(self.addr)
                
                # If all the acceptors return None values, send ACCEPT messages with the value we are
                # trying to set. Else, set value to the highest value returned by the acceptors.
                if highestValue == None:
                    highestValue = state.value
                    
                accept_msg = Message(msg.round, 
                                     Message.ACCEPTOR_ACCEPT,
                                     self.addr,
                                     state.highestBallot, 
                                     {'value': highestValue})
                
#                 print '{0}: {1}'.format(self.addr, accept_msg)
                for (source, _, _) in self.paxosStates[r].responses:
                    self.sendMessage(accept_msg, source)

                # Update the state corresponding to sending the accepts
                newState = PaxosState(r, PaxosRole.PROPOSER, 
                                      PaxosState.PROPOSER_SENT_ACCEPT,  
                                      state.highestBallot,
                                      highestValue)
                self.paxosStates[r] = newState



        
        elif msg.messageType == Message.ACCEPTOR_NACK:
            # If we receive a NACK message from any of the servers, abandon this round
            # because we are never going to succeed with the current ballot number
            
            # Add code to implement the above
            pass
                
        elif msg.messageType == Message.PROPOSER_ACCEPT:
            # Try to get the state for the acceptor
            try: 
                state = self.paxosStates[r]
            except: 
                return
            # Accept the ACCEPT request with the value if we haven't responded to any other 
            # server with a higher ballot
            if msg.ballot >= state.highestBallot:
                newState = PaxosState(r, PaxosRole.ACCEPTOR, 
                                      PaxosState.ACCEPTOR_ACCEPTED,  
                                      msg.ballot,
                                      msg.messageType['value'])
            
            # If we received a newer proposal before getting an accept from the original proposer,
            # send a NACK to the original proposer
            else:
                nack_msg = Message(msg.round, 
                                   Message.ACCEPTOR_NACK, 
                                   self.addr,
                                   msg.ballot, 
                                   {'highestballot': state.highestBallot})
                print '{0}: Sending a NACK to {1}'.format(self.addr, msg.source)
                self.sendMessage(nack_msg, msg.source)


    # Initiate Paxos with a proposal to a quorum of servers
    def initPaxos(self, round, ballot = None, value = None):
        if ballot == None:
            ballot = Ballot(self.addr[0], self.addr[1])
            if round in self.paxosStates:
                print '{0}: Found a previous ballot for this round. Setting current ballot greater than prev ballot.'.format(self.addr)
                ballot.set_n(self.paxosStates[round].highestBallot.n+1)

        prop_msg = Message(round, Message.PROPOSER_PREPARE, self.addr, ballot)
        
        print '{0}: Initiating Paxos for round {1}'.format(self.addr, round)
        for server in self.getQuorum():
            self.sendMessage(prop_msg, server)
    
        self.paxosStates[round] = PaxosState(round, PaxosRole.PROPOSER, 
                                             PaxosState.PROPOSER_SENT_PROPOSAL,  
                                             ballot,
                                             value)
        

    
    # Returns a list of servers other than self that create a quorum
    def getQuorum(self):
        return random.sample(self.serverSet, self.quorumSize-1)
    
    # Serialize and send the given message msg to the given address addr
    def sendMessage(self, msg, addr):
        print '{0}: Sent a message to {1}'.format(self.addr, addr)
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
    
    n3 = Node('127.0.0.1', 55557)
    n3.start()

    time.sleep(2)
#     b = Ballot('127.0.0.1', 55556)
#     msg = Message(0, Message.PROPOSER_PREPARE, n2.addr, b)
#     n2.sendMessage(msg, ('127.0.0.1', 55555))
    n3.initPaxos(0, value = 10)
    time.sleep(2)
    
    time.sleep(2)
    n.initPaxos(0, value = 20)
    time.sleep(2)
    print n.paxosStates[0]

#     for _ in xrange(5):
#         print n.getQuorum()
#         
#     print 
#     
#     for _ in xrange(5):
#         print n2.getQuorum()

#     time.sleep(3)
#     b.increment()
#     msg = Message(0, Message.ACCEPTOR_ACCEPT, n2.addr, b)
#     n2.sendMessage(msg, ('127.0.0.1', 55555))
    
#     prep_msg = Message(0, Message.PROPOSER_PREPARE, n2.addr, b, None)
#     n2.sendMessage(prep_msg, ('127.0.0.1', 55555))


