#!/usr/bin/python

import pickle

class Log():
    DEPOSIT    = 1
    WITHDRAW   = 2
    
    def __init__(self):
        self.transactions = {}

    #Persist the log to disk
    def save(self):
        try:
            with open('log.dat', 'wb') as file:
                pickle.dump(self.transactions, file)
                return True

        except Exception as e:
            return False

    #Read the log from disk
    def restore(self):
        try:
            with open('log.dat', 'rb') as file:
                self.transactions = pickle.load(file)
                print "Found existing log:\n", self, "\n"
                return True

        except Exception as e:
            return False

    def appendTransaction(self, type, value, roundNum):
        if roundNum in self.transactions:
            print "OVERWRITTING EXISTING TRANSACTION #" + str(roundNum)
            
            self.transactions[roundNum] = (type, value)
            self.save()

    def history(self):
        for key in self.transactions:
            if self.transactions[key].type == Log.DEPOSIT:
                print '\nDeposit:  ${0}'.format(self.transactions[key].value)

            elif self.transactions[key].type == Log.WITHDRAW:
                print '\nWithdraw: ${0}'.format(self.transactions[key].value)


    def __str__(self):
        return ('Num transactions:       {0}\n'
                'Transactions:           {1}\n'.format(len(self.transactions),
                                                self.transactions))



if __name__ == '__main__':
    l = Log()
    l.restore()
    l.appendTransaction(Log.DEPOSIT, 1000, 1)
    l.appendTransaction(Log.WITHDRAW, 200, 2)
    l.appendTransaction(Log.WITHDRAW, 300, 3)
    l.appendTransaction(Log.DEPOSIT, 700, 4)
    print l


