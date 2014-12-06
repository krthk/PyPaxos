#!/usr/bin/python

import pickle

class Log():
    DEPOSIT    = 1
    WITHDRAW   = 2
    
    def __init__(self):
        self.transactions = {}
        self.nextTransationNum = 1
    
    def addTransaction(self, type, value):
        self.transactions[self.nextTransationNum] = (type, value)
        self.nextTransationNum += 1
    
    #Delete a single transaction
    def deleteTransaction(self, transactionNum):
        if transactionNum in self.transactions:
            del self.transactions[transactionNum]
    
    #Delete all transactions less than the specified transaction num
    def deleteTransactionsUpToTransactionNum(self, transactionNum):
        for key in range(1, transactionNum):
            if key in self.transactions:
                self.deleteTransaction(key)

    #Persist the log to disk
    def save(self):
        try:
            with open('log.dat', 'wb') as file:
                pickle.dump(self.transactions, file)

        except Exception as e:
            print e

    #Read the log from disk
    def restore(self):
        try:
            with open('log.dat', 'rb') as file:
                self.transactions = pickle.load(file)
                self.nextTransationNum = max(self.transactions.iterkeys())+1
                print "Found existing log:\n", self, "\n"

        except Exception as e:
            print e


    def __str__(self):
        return ('Num transactions:       {0}\n'
                'Next transaction num:   {1}\n'
                'Transactions:           {2}\n'.format(len(self.transactions),
                                                self.nextTransationNum,
                                                self.transactions))



if __name__ == '__main__':
    l = Log()
    l.restore()
    l.addTransaction(Log.DEPOSIT, 1000)
    l.addTransaction(Log.WITHDRAW, 200)
    l.addTransaction(Log.WITHDRAW, 300)
    l.addTransaction(Log.DEPOSIT, 700)
    print l
    l.deleteTransaction(2)
    print l
    l.deleteTransactionsUpToTransactionNum(100)
    print l
    l.addTransaction(Log.WITHDRAW, 300)
    print l
    l.addTransaction(Log.DEPOSIT, 700)
    print l
    l.addTransaction(Log.DEPOSIT, 1000)
    print l
    l.save()


