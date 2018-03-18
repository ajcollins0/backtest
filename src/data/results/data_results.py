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

    def add_trade(self, entry_date, entry_price, exit_date, exit_price):
        t = Trade(entry_date, entry_price, exit_date, exit_price)
        self.trades.append(t)

    def print_results(self, full=False, graph=False, monte=True):

        capital = 10000
        
        monte_median = 0.0

        w_arr = np.array([])
        l_arr = np.array([])

        w_count = 0
        l_count = 0

        for i in self.trades:
            if i.exit_price > i.entry_price:
                w_count += 1
                trade_res = (i.exit_price - i.entry_price) / i.entry_price
                capital = capital + capital * trade_res
                w_arr = np.append(w_arr, trade_res)
            else:
                trade_res = (i.entry_price - i.exit_price) / i.entry_price
                capital = capital - capital * trade_res
                l_arr = np.append(l_arr, trade_res)
                l_count += 1

        num_trades = len(self.trades)
        win_per = float(w_count)/float(len(self.trades))
        ave_win = w_arr.mean()
        ave_loss = l_arr.mean()

        print "Number of trades:", num_trades
        print "Win Percentage:", win_per
        print "Finishing Capital:", capital

        print
        print "Mean Win", ave_win
        print "Mean Loss", ave_loss
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

        if monte:
            monte_median = self.__monte_test(num_trades, win_per, ave_win, ave_loss)

        if graph:
            gh.graph_results(self.trades)

        print 
        print capital, monte_median, num_trades, win_per, ave_win, ave_loss

    def __monte_test(self, num_trades, win_per, ave_win, ave_loss):
        
        monte_results = np.array([])
        numTests = 10000
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

