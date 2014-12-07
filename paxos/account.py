#!/usr/bin/python

class Account(object):
    balance = 0.0

    #Check the balance
    def getBalance(self):
        print ("Your balance is $%.2f" % self.balance)
        return round(self.balance, 2)

    #Deposit
    def deposit(self, amount):
        self.balance += round(amount, 2)
        print "Funds deposited"
        return True
    
    #Withdraw if amount is available
    def withdraw(self, amount):
        amount = round(amount, 2)
        
        if self.balance >= amount:
            self.balance -= amount
            print "Funds withdrawn"
            return True
        
        else:
            print "Not enough funds available for this withdrawal"
            return False
    
    # Check if we have sufficient balance for withdrawal
    def isSufficient(self, amount):
        return self.balance >= amount



