import sqlite3
import csv
from stock import Day
from pylab import date2num
from datetime import datetime, time, date

class DataQueryDB:

    # defin DB params
    def __init__(self):
        self.cur = None
        self.conn = None

    def set_db(self, db_path):
        self.conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.conn.cursor()

    def get_tickers(self):
        cmd = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cur.execute(cmd)
        tickers = []
        for i in self.cur.fetchall():
            tickers.append(i[0].strip()[:-6])
        return tickers

    def get_stock_data(self, tickers):
        ret_val = {}
        for ticker in tickers:
            cmd = "SELECT * FROM %s" % (ticker + "_OHLCV")
            self.cur.execute(cmd)
            t = []
            for d in self.cur.fetchall():
                td = datetime.combine(d[0],  datetime.min.time())
                a = Day(date2num(td), d[1], "0:0", d[2], d[3], d[4], d[5])
                t.append(a)
            ret_val[ticker] = t
        return ret_val

    def close_db(self):
        self.cur.close()
        self.conn.close()

class DataQuery:

    # set where to pull data from
    def __init__(self, path):
        self.path = path

    def get_stock_data(self, tickers, after_hours=False, start_date=None, end_date=None):
        
        start_time = time(9, 30)
        # the candle counts as 30 min, so we end our time at the last candle, starting at 3:30pm EST
        end_time = time(15, 30)

        if start_date is None:
            start_date=date(1990,1,1)

        if end_date is None:
            end_date=date(3000,1,1)

        ret_val = {}
        for ticker in tickers:
            t = []
            with open(self.path + ticker + '.txt', 'rb') as f:
                reader = csv.reader(f)
                for row in reader:
                    data_date = datetime.strptime(row[0], "%m/%d/%Y")
                    if data_date.date() >= start_date and data_date.date() <= end_date:
                        if len(row) == 7:
                            time_arr=row[1].split(":")
                            cur_time = time(int(time_arr[0]),int(time_arr[1]))
                            if after_hours:
                                t.append(Day(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                            else:
                                if cur_time >= start_time and cur_time <= end_time:
                                    t.append(Day(row[0], row[1], row[2],row[3],row[4],row[5],row[6]))
                        elif len(row) == 6:
                            t.append(Day(row[0],"0:0",row[1],row[2],row[3],row[4],row[5])) 
            ret_val[ticker] = t
        return ret_val
