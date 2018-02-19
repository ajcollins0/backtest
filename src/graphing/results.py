import sys
import operator
from collections import OrderedDict
from pylab import num2date
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import matplotlib.pyplot as plt


def __get_graphing_data(trades, i, comm, starting_equity):
    # loop over trades list and calculate equity from every trade
    #  for multiple trades in one day, we devide our total equity by the number
    #  of trades in the given day and use this rather than the total equity in the trade
    dates = []
    equity = []
    eq = starting_equity
    od = OrderedDict()
    for j in sorted(trades[i], key=operator.attrgetter('exit_date')):
        if j.exit_date not in od:
            od[j.exit_date] = [j.result_per]
        else:
            od[j.exit_date].append(j.result_per)
    for k in od:
        dates.append(k)
        if len(od[k]) > 1:
            pre_eq = eq / float(len(od[k]))
            sumer = 0
            for l in od[k]:
                addr = pre_eq * (l / 100.)
                p = pre_eq + addr - (2 * comm)
                temp_eq = p if p > 0. else 0.
                sumer += temp_eq
            eq = sumer
        else:
            addr = eq * (od[k][0] / 100.)
            p = eq + addr - (2 * comm)
            eq = p if p > 0. else 0.
        equity.append(eq)
    return dates, equity


def __print_trades(trades, i, comm, starting_equity):
    # loop over the trades and dump the trade/equity information
    # this can't be with __get_graphing_data since this is used for the best strat
    eq = starting_equity
    od = OrderedDict()
    for j in sorted(trades[i], key=operator.attrgetter('exit_date')):
        if j.exit_date not in od:
            od[j.exit_date] = [j]
        else:
            od[j.exit_date].append(j)
    for k in od:
        if len(od[k]) > 1:
            pre_eq = eq / float(len(od[k]))
            sumer = 0
            for l in od[k]:
                addr = pre_eq * (l.result_per / 100.)
                p = pre_eq + addr - (2 * comm)
                temp_eq = p if p > 0. else 0.
                sumer += temp_eq
                eq = sumer
                print("%-15.3f%-15.3f%-15s%-15s%-15s%-15.3f%-15.3f") % (eq, l.result_per, num2date(
                    l.entry_date).date(), num2date(l.exit_date).date(), l.ticker,
                    l.entry_price, l.exit_price)
        else:
            l = od[k][0]
            addr = eq * (l.result_per / 100.)
            p = eq + addr - (2 * comm)
            eq = p if p > 0. else 0.
            print("%-15.3f%-15.3f%-15s%-15s%-15s%-15.3f%-15.3f") % (eq, l.result_per, num2date(
                l.entry_date).date(), num2date(l.exit_date).date(), l.ticker,
                l.entry_price, l.exit_price)


def __get_best_strat(trades, comm, starting_equity):
    # returns graphing requirements to plot the equity of the best performing strat
    days = []
    ave_pls = []
    averages = []
    best_equity = 0
    best_trades = 0
    best_dates = []
    best_trades_index = 0

    for i in range(0, len(trades)):
        trs = [j.result_per for j in trades[i]]
        if len(trs) > 0:
            ws = [j for j in trs if j > 0]
            ls = [j for j in trs if j <= 0]
            days.append(i + 1)
            ave_pl = np.average(ws) / abs(np.average(ls))
            wsp = float(len(ws)) / float(len(trs))
            ave_pls.append(ave_pl)
            averages.append(wsp)
            temp_dates, temp_equity = __get_graphing_data(
                trades, i, comm, starting_equity)
            if temp_equity[len(temp_equity) - 1] >= best_equity:
                best_equity = temp_equity[len(temp_equity) - 1]
                best_trades = temp_equity
                best_dates = temp_dates
                best_trades_index = i
            if i == 0:
                print("%-10s%-10s%-12s%-12s%-10s") % ("Length", "Trades", "Perc", "Ave P/L",
                                                      "Final Equity")
            if len(trs) > 0:
                print("%-10d%-10d%-12.3f%-12.3f%-30.3f") % (i + 1, len(trs), float(len(ws)) / float(len(trs)),
                                                            ave_pl, temp_equity[len(temp_equity) - 1])
            else:
                print("%-10d") % (i + 1)

    return days, ave_pls, averages, best_dates, best_trades, best_trades_index


def graph_results(trades, spy_overlay=False,
                  print_trades=False, comm=5., starting_equity=10000.,
                  file_name=None):
    # prints equity, aveP/L and win% from a list of trades, use comm, and
    # starting_equity to best estimate real life sitautions

    if file_name:
        sys.stdout = open(file_name + '_Trade_Table.txt', 'w')

    days, ave_pls, averages, best_dates, best_trades, best_trades_index = __get_best_strat(
        trades, comm, starting_equity)

    if print_trades:
        __print_trades(trades, best_trades_index, comm, starting_equity)

    fig = plt.figure(figsize=(14, 6))
    fig.canvas.set_window_title('Profit / Loss')
    fig2 = plt.figure(2, figsize=(14, 6))
    fig2.canvas.set_window_title('Averages')
    fig3 = plt.figure(3, figsize=(14, 6))
    fig3.canvas.set_window_title(
        'Equity Curve - Best Days Held ' + str(best_trades_index + 1))

    ax1 = fig.add_subplot(1, 1, 1)
    ax2 = fig2.add_subplot(1, 1, 1)
    ax3 = fig3.add_subplot(1, 1, 1)

    # format y axis for %
    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

    # format y axis for $
    if (max(best_trades) / starting_equity) > 50:
        ax3.set_yscale("log")
    ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    # make dates readable
    ax3.xaxis_date()
    ax3.autoscale_view()
    # set plots
    ax1.plot(days, ave_pls, linewidth=2)
    ax2.plot(days, averages, linewidth=2)
    ax3.plot(best_dates, best_trades)

    # labels
    ax1.set_ylabel('Average P/L', size=20)
    ax2.set_ylabel('Win/Loss Percentage', size=20)
    ax3.set_ylabel('Equity($)', size=20)
    ax1.set_xlabel('Days Held', size=20)
    ax2.set_xlabel('Days Held', size=20)
    ax3.set_xlabel('Dates Traded', size=20)

    if spy_overlay:
        ax4 = ax3.twinx()
        ax4.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        from engine.database import db
        # note: current python path is where prog was intially ran
        cur, conn = db.get_cursor('stock.db')
        data = db.get_ticker_data(cur, "SPY")
        conn.close()
        clses = []
        ddd = []
        for i in range(0, len(data)):
            if data[i][0] >= best_dates[0]:
                clses.append(data[i][4])
                ddd.append(data[i][0])
        ax4.plot(ddd, clses, 'r-', alpha=.6)
        ax4.set_ylabel('SPY Close ($)', color='r', size=20)

    if file_name:
        f = '%.2f' % best_trades[len(best_trades) - 1]
        file_name = f + '_' + file_name
        fig.savefig(file_name + '_Profit_Loss.png')
        fig2.savefig(file_name + '_Win_Loss.png')
        fig3.savefig(file_name + '_Equity.png')
    else:
        plt.show()
