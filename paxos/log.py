#!/usr/bin/python

import pickle

class Log():
    DEPOSIT    = 1 
    WITHDRAW   = 2
    
    def __init__(self, ip, port):
        self.filename = 'paxos-' + str(ip) + str(port)+ '.log'
        self.transactions = []
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
                
                for transaction in self.transactions:
                    print transaction
                    if transaction[0] == Log.DEPOSIT:
                        self.balance += transaction[1]
                
                    elif transaction[0] == Log.WITHDRAW:
                        self.balance -= transaction[1]
                
                return True

        except Exception as e:
            return False

    def appendTransaction(self, type, value, hash):
        if type == Log.DEPOSIT:
            self.balance += value

        elif type == Log.WITHDRAW:
            self.balance -= value

        self.transactions.append((type, value, hash))
        self.save()

    def history(self):
        if len(self.transactions) == 0:
            print '[ EMPTY ]'
        
        for transaction in self.transactions:
            if transaction[0] == Log.DEPOSIT:
                print 'Deposit:  ${0}'.format(transaction[1])

            elif transaction[0] == Log.WITHDRAW:
                print 'Withdraw: ${0}'.format(transaction[1])

    def __str__(self):
        return ('Num transactions:       {0}\n'
                'Transactions:           {1}\n'.format(len(self.transactions),
                                                self.transactions))



if __name__ == '__main__':
    l = Log()
    l.appendTransaction(Log.DEPOSIT, 1000, 1)
    l.appendTransaction(Log.WITHDRAW, 200, 2)
    l.appendTransaction(Log.WITHDRAW, 300, 3)
    l.appendTransaction(Log.DEPOSIT, 700, 4)
    l.history()
    print l


