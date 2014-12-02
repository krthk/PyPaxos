#!/usr/bin/python

import sys
import threading
import helper
from account import Account
from node import Node


#Get the arguments
if len(sys.argv) != 1:
    print ""
    print "Usage: %s <port>" % str(sys.argv[0])
    print ""
    sys.exit(0)


#Create Node object
node = Node()

#Create Account object
account = Account()

#Threaded networking process
def setupServer():
    server.setup()

#Start the background networking
thread = threading.Thread(target=setupServer, args = ())
thread.daemon = True
thread.start()


#Main loop of application
while True:
    #Get user input
    input = raw_input("\n> ")
    
    #End application
    if input == "quit":
        sys.exit(0)
    
    if input == "help":
        print "\n------------------------------------------------\n"
        print "balance"
        print "  - Returns the current balance\n"
        print "deposit <amount>"
        print "  - Increments the current balance by <amount>\n"
        print "withdraw <amount>"
        print "  - Decrements the current balance by <amount>\n"
        print "fail"
        print "  - Simulates a node failure\n"
        print "unfail"
        print "  - Starts node after fail was called\n"
        print "------------------------------------------------"
        continue


    #Split the input into args
    args = input.split()

    if len(args) == 1:
        args[0] = args[0].lower()
        
        if args[0] == "balance":
            account.getBalance()

        elif args[0] == "fail":
            print "IMPLEMENT"
                
        elif args[0] == "unfail":
            print "IMPLEMENT"
            
    elif len(args) == 2:
        args[0] = args[0].lower()
        
        #Make sure second arg is a numberical value
        if helper.isNumber(args[1]):
            amount = float(args[1])
            
            if args[0] == "deposit":
                account.deposit(amount)
                
                message = "Deposited $%.2f" % amount
                node.send(message, "127.0.0.1", 55555)

            elif args[0] == "withdraw":
                account.withdraw(amount)
    
        else:
            print "Invalid amount"






