#!/usr/bin/env python

from data.db import DataQuery
from data.results.data_results import Results as res
from data.indicators import inc
from graphing import graph as gh

import numpy as np

if __name__ == '__main__':

    a = DataQuery('../dataset/daily/')

    #  get stock data
    tickers = a.get_stock_data(['SPY'])

    results = res()

    hold = 7
    c = 0
    b = 0
    for key, tix in tickers.iteritems():
        for idx, val in enumerate(tix):
            if inc.consec_down(idx,tix,2) and idx + hold < len(tix):
                results.add_trade(tix[idx].date, tix[idx].close, tix[idx+hold].date, tix[idx+hold].close)
                # if idx>80:
                #     print val.get_date(), idx, val.close
                #     gh.graph_space_trade(tickers["SPY"],idx,idx+5)
                #     quit()

                # c += 1
                # if idx+1<len(tix):
                #     if inc.is_up_day(tix[idx+1]):
                #         b += 1
                #         arr = np.append(arr,inc.daily_percent_gain(idx+1,tix))

    results.print_results()
    # gh.graph_space_trade(tickers["SPY"],134,155)

    # print "all up days", c
    # print "day after up day", b


    # for x in np.nditer(arr):
    #     print x

