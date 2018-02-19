import numpy as np
import matplotlib.pyplot as plt
from pylab import num2date, savefig
from matplotlib.finance import candlestick2_ohlc, candlestick_ohlc, volume_overlay, quotes_historical_yahoo_ohlc
from matplotlib.transforms import Bbox
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from pylab import num2date, date2num

def get_data_arrays(data):
    # format data pieces:
    opens = []
    highs = []
    lows = []
    closes = []
    vols = []
    for i in data:
        opens.append(i.open)
        highs.append(i.high)
        lows.append(i.low)
        closes.append(i.close)
        vols.append(i.volume)

    return opens,highs,lows,closes,vols

def graph(data):

    opens,highs,lows,closes,vols = get_data_arrays(data)

    # create new plot
    fig = plt.figure(figsize=(14, 6))

    ax1 = fig.add_subplot(1, 1, 1)
    
    # plt.gcf().subplots_adjust(top=.95, bottom=0.17, left=.10, right=.85)
    plt.gcf().subplots_adjust(left=.10, right=.85)

    # plot price chart
    candlestick2_ohlc(ax1, opens, highs, lows, closes,
                      alpha=1, width=1, colorup='g', colordown='r')

    # remove useless x axis ticks
    ax1.get_xaxis().set_ticks([])

    # pad y axis of the price chart to avoide collisions with volume overlay
    y_lim = ax1.get_ylim()
    ax1.set_ylim(y_lim[0] - (.27 * (y_lim[1] - y_lim[0])), y_lim[1])
    
    # turn on grid - only print horiztonal
    ax1.yaxis.grid(True)

    # format ax1's y axis ticks
    y_lim = ax1.get_ylim()
    majorLocator = MultipleLocator(float((y_lim[1] - y_lim[0]) / 10))
    majorFormatter = FormatStrFormatter('%.2f')
    ax1.yaxis.set_major_locator(majorLocator)
    ax1.yaxis.set_major_formatter(majorFormatter)

    # print label of price chart
    ax1.set_ylabel('Price', size=20)

    # Add a seconds axis for the volume overlay
    ax2 = ax1.twinx()

    # scale the x-axis to show all points without cutoff
    ax1.set_xlim(0 - 0.5, len(opens) - 0.5)
    ax2.set_xlim(0 - 0.5, len(opens) - 0.5)

    # Plot the volume overlay
    volume_overlay(ax2, opens, closes, vols, colorup='g', colordown='r',
                   width=1)

    # shrink the y axis of the volume overlay
    pos = ax2.get_position()
    ax2.set_position(Bbox([[pos.x0, pos.y0], [pos.x1, 0.27]]))

    # print label of volume overlay
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Volume', size=10)

    # remove sciientific notation and reduce amount of ticks
    ax2.get_yaxis().get_major_formatter().set_scientific(False)
    ax2.set_yticks(ax2.get_yticks()[::2])

    # remove top border of volume overlay
    ax2.spines['top'].set_visible(False)

    plt.show()


def graph_trade(data, entry, exit, padding=5):
    start = max(0, entry - padding)
    finish = min(len(data) - 1, exit + padding)
    graph(data[start:finish])

def get_data_array(data):
    # format data pieces:

    ret_val = []
    for i in data:
        ret_val.append([i.get_date_num(), i.open,i.high,i.low,i.close,i.volume])

    return ret_val

def graph_space(data):

    data = get_data_array(data)

    # create new plot
    fig = plt.figure(figsize=(14, 6))
    ax1 = fig.add_subplot(1, 1, 1)
    plt.gcf().subplots_adjust(top=.95, bottom=0.17, left=.10, right=.85)

    # plot price chart
    candlestick_ohlc(
        ax1, data, alpha=1, width=1, colorup='g',
        colordown='r')

    # pad y axis of the price chart to avoide collisions with volume overlay
    y_lim = ax1.get_ylim()
    ax1.set_ylim(y_lim[0] - (.27 * (y_lim[1] - y_lim[0])), y_lim[1])
    # turn on grid - only print horiztonal
    ax1.yaxis.grid(True)

    # format ticks
    y_lim = ax1.get_ylim()
    majorLocator = MultipleLocator(float((y_lim[1] - y_lim[0]) / 10))
    majorFormatter = FormatStrFormatter('%.2f')
    ax1.yaxis.set_major_locator(majorLocator)
    ax1.yaxis.set_major_formatter(majorFormatter)

    # print label of price chart
    ax1.set_ylabel('Price', size=20)

    # make dates readable
    ax1.xaxis_date()
    ax1.autoscale_view()
    plt.xticks(rotation=45, horizontalalignment='right')

    # Add a seconds axis for the volume overlay
    ax2 = ax1.twinx()

    # get array of dates
    dates = [i[0]for i in data]

    # scale the x-axis to show all points without cutoff
    ax1.set_xlim(min(dates) - 0.5, max(dates) + 0.5)
    ax2.set_xlim(min(dates) - 0.5, max(dates) + 0.5)

    # get lists of postive and negitive dates
    pos_dates = []
    neg_dates = []
    pos_vols = []
    neg_vols = []
    for i in range(0, len(data)):
        if data[i][1] - data[i][4] <= 0:
            pos_dates.append(data[i][0])
            pos_vols.append(data[i][5])
        else:
            neg_dates.append(data[i][0])
            neg_vols.append(data[i][5])

    # Plot the volume overlay
    ax2.bar(pos_dates, pos_vols, color='green', width=1, align='center')
    ax2.bar(neg_dates, neg_vols, color='red', width=1, align='center')

    # shrink the y axis of the volume overlay
    pos = ax2.get_position()
    ax2.set_position(Bbox([[pos.x0, pos.y0], [pos.x1, 0.35]]))

    # print label of volume overlay
    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Volume', size=10)

    # remove sciientific notation and reduce amount of ticks
    ax2.get_yaxis().get_major_formatter().set_scientific(False)
    ax2.set_yticks(ax2.get_yticks()[::2])

    # remove top border of volume overlay
    ax2.spines['top'].set_visible(False)

    plt.show()


def graph_space_trade(data, entry, exit, padding=5):
    # exit has to be entry + trade length
    start = max(0, entry - padding)
    finish = min(len(data) - 1, exit + padding)
    graph_space(data[start:finish])

def graph_results(results):

    w_res = []
    l_res = []
    w_x = []
    l_x = []
    z = []
    z_x = []
    for i in results:
        percent_change = (i.exit_price - i.entry_price) * 100.0 / i.entry_price
        if percent_change > 0:
            w_res.append(percent_change)
            w_x.append(i.entry_date)
        else:
            l_res.append(percent_change)
            l_x.append(i.entry_date)
        z.append(0)
        z_x.append(i.entry_date)

    plt.plot(w_x, w_res, 'go', ms=3)
    plt.plot(l_x, l_res, 'ro', ms=3)
    plt.plot(z_x, z, ls='-',c='black', ms=1)

    plt.show()
