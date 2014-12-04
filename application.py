#!/usr/bin/python

import sys
import threading
import time
import helper
from account import Account
from node import Node


#Get the arguments
if len(sys.argv) != 1:
    print ""
    print "Usage: %s <port>" % str(sys.argv[0])
    print ""
    sys.exit(0)


#Create Account object
account = Account()

#Create Node object
node = Node()
node.daemon = True
node.start()

#Wait a moment for the node to get its socket set up
time.sleep(1)



#Main loop of application
while True:
    #Get user input
    input = raw_input("\n> ")
    
    #End application
    if input == "quit":
        sys.exit(0)
    
    if input == "help":
        print "\n------------------------------------------------\n"
        print "(b)alance"
        print "  - Returns the current balance\n"
        print "(d)eposit <amount>"
        print "  - Increments the current balance by <amount>\n"
        print "(w)ithdraw <amount>"
        print "  - Decrements the current balance by <amount>\n"
        print "(f)ail"
        print "  - Simulates a node failure\n"
        print "(u)nfail"
        print "  - Starts node after fail was called\n"
        print "------------------------------------------------"
        continue


    #Split the input into args
    args = input.split()

    if len(args) == 1:
        args[0] = args[0].lower()
        
        if args[0] == "b" or args[0] == "balance":
            account.getBalance()

        elif args[0] == "f" or args[0] == "fail":
            node.fail()
                
        elif args[0] == "u" or args[0] == "unfail":
            node.unfail()
            
    elif len(args) == 2:
        args[0] = args[0].lower()
        
        #Make sure second arg is a numberical value
        if helper.isNumber(args[1]):
            amount = float(args[1])
            
            if args[0] == "d" or args[0] == "deposit":
                account.deposit(amount)
                
                node.createPaxosRound()

            elif args[0] == "w" or args[0] == "withdraw":
                account.withdraw(amount)
    
        else:
            print "Invalid amount"






