import numpy as np
from graphing import graph as gh
from random import random

class Trade:

    def __init__(self):
        self.entry_date = None
        self.exit_date = None
        self.entry_price = None
        self.exit_price = None

    def __init__(self, entry_date, entry_price, exit_date, exit_price):
        self.entry_date = entry_date
        self.exit_date = exit_date
        self.entry_price = entry_price
        self.exit_price = exit_price

class Results:

    def __init__(self):
        self.trades = []
        self.num_trades = None
        self.win_per = None
        self.ave_win = None
        self.ave_loss = None
        self.win_median = None 
        self.lose_median = None

    def add_trade(self, entry_date, entry_price, exit_date, exit_price):
        t = Trade(entry_date, entry_price, exit_date, exit_price)
        self.trades.append(t)

    def print_results(self, full=False, graph=False, monte=True, m_size=10000):

        monte_median = 0.0

        w_arr = np.array([])
        l_arr = np.array([])
        all_trades = []

        for i in self.trades:
            trade_return = (i.exit_price - i.entry_price) / i.entry_price
            all_trades.append(trade_return)
            if trade_return > 0:
                w_arr = np.append(w_arr, trade_return)
            else:
                l_arr = np.append(l_arr, trade_return)

        self.num_trades = len(self.trades)
        self.win_per = float(len(w_arr))/float(len(self.trades))
        self.ave_win = w_arr.mean()
        self.ave_loss = l_arr.mean()
        self.win_median = np.median(w_arr)
        self.lose_median = np.median(l_arr)

        print "Number of trades:", self.num_trades
        print "Win Percentage:", self.win_per

        print
        print "Mean Win", self.ave_win
        print "Mean Loss", self.ave_loss
        print 
        print "Median Win", self.win_median
        print "Median Loss", self.lose_median
        print 
        print "Max Win", np.amax(w_arr)
        print "Max Loss", np.amin(l_arr)
        
        if full:
            print 
            print "Min Win", np.amin(w_arr)
            print "Min Loss", np.amax(l_arr)
        print 
        print "Standard Deviation of Wins", np.std(w_arr, ddof=1)
        print "Standard Deviation of Loses", np.std(l_arr, ddof=1)
        print
        print "Number of wins:", len(w_arr)
        print "Number of loses:", len(l_arr)

        c_ret = 1
        for i in all_trades:
            n = 1+i
            c_ret = c_ret * n

        c_ret=c_ret-1

        print "Compouned Return", c_ret

        if monte:
            monte_median = self.__monte_test(num_trades, win_per, ave_win, ave_loss, monte_size=m_size)

        if graph:
            gh.graph_results(self.trades)

        print 
        print str(monte_median)+","+ str(self.num_trades)+","+ str(self.win_per)+","+ str(self.ave_win)+","+ str(self.ave_loss)

    def __monte_test(self, num_trades, win_per, ave_win, ave_loss, monte_size):
        
        monte_results = np.array([])
        numTests = monte_size
        startingCapital = 10000.0

        for t in range(numTests):
            capital = startingCapital
            for i in range(num_trades):
                if random() <= win_per:
                    capital  = capital + (capital*ave_win)
                else:
                    capital = capital - (capital*ave_loss)
            monte_results = np.append(monte_results, capital)

        print
        print "Monte Carlo Results"
        print "  mean:", np.mean(monte_results)
        print "  median:",  np.median(monte_results)
        print "  std dev:", np.std(monte_results, ddof=1)
        print "  max:", np.amax(monte_results)
        print "  min:", np.amin(monte_results)

        return np.median(monte_results)

