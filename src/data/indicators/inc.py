import numpy as np

# returns true if day is up
def is_up_day(day):
    if day.close > day.open:
        return True

# returns true if day is down
def is_down_day(day):
    if day.open > day.close:
        return True

def consec_down(idx, data, num_days):
    if num_days == 1:
        return is_down_day(data[idx])
    else:
        if idx - num_days + 1 <= 0:
            return False
        i = idx
        for i  in range(idx - num_days + 1, idx+1):
            if not is_down_day(data[i]):
                return False
            i=-1
        return True

def consec_up(idx, data, num_days):
    if num_days == 1:
        return is_up_day(data[idx])
    else:
        if idx - num_days + 1 <= 0:
            return False
        i = idx
        for i  in range(idx - num_days + 1, idx+1):
            if not is_up_day(data[i]):
                return False
            i=-1
        return True

def open_higher_than_prev_close(idx, data):
    if idx - 1 < 0:
        return False
    else:
        if data[idx].open > data[idx - 1].close:
            return True
        else:
            return False

def open_lower_than_prev_close(idx, data):
    if idx - 1 < 0:
        return False
    else:
        if data[idx].open < data[idx - 1].close:
            return True
        else:
            return False

def daily_percent_gain(idx, data):
    return (data[idx].close - data[idx].open) * 100.0 / data[idx].close

def day_over_day_percent_gain(idx, data):
    if idx - 1 < 0:
        return 0.0
    else:
        return (data[idx].close - data[idx-1].close) * 100.0 / data[idx].close

def opening_percent_gain(idx, data):
    if idx - 1 < 0:
        return 0.0
    else:
        return (data[idx].open - data[idx-1].close) * 100.0 / data[idx-1].close

def get_closes_array(data):
    arr = []
    for i in data:
        arr.append(i.close)
    return arr

def sma(data, N):
    closes = get_closes_array(data)
    cumsum = np.cumsum(np.insert(closes, 0, 0))
    smas = (cumsum[N:] - cumsum[:-N]) / float(N)
    for i in range(len(closes) - len(smas)):
            smas = np.insert(smas,0,0)
    return smas
