#!/usr/bin/python

import pickle

class Log():
    DEPOSIT    = 1
    WITHDRAW   = 2
    
    def __init__(self):
        self.transactions = {}
    
    def appendTransaction(self, type, value, roundNum):
        if roundNum in self.transactions:
            print "OVERWRITTING TRANSACTION #" + str(roundNum)
        
        self.transactions[self.roundNum] = (type, value)
        self.save()
    

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
    l.appendTransaction(Log.DEPOSIT, 1000, 1)
    l.appendTransaction(Log.WITHDRAW, 200, 2)
    l.appendTransaction(Log.WITHDRAW, 300, 3)
    l.appendTransaction(Log.DEPOSIT, 700, 4)
    print l


