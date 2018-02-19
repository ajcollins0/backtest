import numpy as np
from graphing import graph as gh

class Trade:

    def __init__(self):
        self.entry_date = ''
        self.exit_date = ''
        self.entry_price = 0.0
        self.exit_price = 0.0

    def __init__(self, entry_date, entry_price, exit_date, exit_price):
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.entry_price = entry_price
        self.exit_price = exit_price

class Results:

    def __init__(self):
        self.trades = []

    def add_trade(self, entry_date, entry_price, exit_date, exit_price):
        t = Trade(entry_date, entry_price, exit_date, exit_price)
        self.trades.append(t)

    def print_results(self, full=True, graph=True, monte=True):

        w_arr = np.array([])
        l_arr = np.array([])

        w_count = 0
        l_count = 0

        for i in self.trades:
            if i.exit_price > i.entry_price:
                w_count += 1
                w_arr = np.append(w_arr, (i.exit_price - i.entry_price) * 100.0 / i.entry_price)
            else:
                l_arr = np.append(l_arr, (i.entry_price - i.exit_price) * 100.0 / i.entry_price)
                l_count += 1

        print "Number of trades:", len(self.trades)
        print "Win Percentage:", float(w_count)/float(len(self.trades))
        print
        print "Mean Win", w_arr.mean()
        print "Mean Loss", l_arr.mean()
        print 
        print "Median Win", np.median(w_arr)
        print "Median Loss", np.median(l_arr)
        print 
        print "Max Win", np.amax(w_arr)
        print "Max Loss", np.amax(l_arr)
        if full:
            print 
            print "Min Win", np.amin(w_arr)
            print "Min Loss", np.amin(l_arr)
        print 
        print "Standard Deviation of Wins", np.std(w_arr, ddof=1)
        print "Standard Deviation of Loses", np.std(l_arr, ddof=1)
        print
        print "Number of wins:", w_count
        print "Number of loses:", l_count

        if graph:
            gh.graph_results(self.trades)


