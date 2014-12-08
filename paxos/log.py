#!/usr/bin/python

import pickle

class Log():
    DEPOSIT    = 1 
    WITHDRAW   = 2
    
    def __init__(self, ip, port):
        self.filename = 'paxos-' + str(ip) + str(port)+ '.log'
        self.transactions = {}
        self.balance = 0
        self.restore()

    #Persist the log to disk
    def save(self):
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump(self.transactions, file)
                return True

        except Exception as e:
            return False

    #Read the log from disk
    def restore(self):
        try:
            with open(self.filename, 'rb') as file:
                self.transactions = pickle.load(file)
                print 'Found existing log: \n{0}'.format(self)
                
                for key in sorted(iter(self.transactions)):
                    print transaction
                    if self.transactions[key][0] == Log.DEPOSIT:
                        self.balance += self.transactions[key][1]
                
                    elif self.transactions[key][0] == Log.WITHDRAW:
                        self.balance -= self.transactions[key][1]
                
                return True

        except Exception as e:
            return False

    def addTransaction(self, round, type, value, hash):
        if type == Log.DEPOSIT:
            self.balance += value

        elif type == Log.WITHDRAW:
            self.balance -= value

        self.transactions[round] = (type, value, hash)
        self.save()

    def history(self):
        if not self.transactions:
            print '[ EMPTY ]'

        for key in sorted(iter(self.transactions)):
            if self.transactions[key][0] == Log.DEPOSIT:
                print '{0} - Deposit:  ${1}'.format(key, self.transactions[key][1])

            elif self.transactions[key][0] == Log.WITHDRAW:
                print '{0} - Withdraw: ${1}'.format(key, self.transactions[key][1])

    def __str__(self):
        return ('Num transactions:       {0}\n'
                'Transactions:           {1}\n'.format(len(self.transactions),
                                                self.transactions))



if __name__ == '__main__':
    l = Log('127.0.0.1', 55555)
    l.addTransaction(0,Log.DEPOSIT, 1000, 1)
    l.addTransaction(2,Log.WITHDRAW, 200, 2)
    l.addTransaction(1,Log.WITHDRAW, 300, 3)
    l.addTransaction(3,Log.DEPOSIT, 700, 4)
    l.history()
    print l


