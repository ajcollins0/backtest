from pylab import num2date, date2num
from datetime import datetime

class Day:

    def __init__(self, date, time, open, high, low, close, volume):
        
        datetime_object = datetime.strptime(date, "%m/%d/%Y")
        self.date = datetime_object 
        self.time = time   
        self.open = float(open)
        self.high = float(high)  
        self.low = float(low)    
        self.close = float(close)
        self.volume = long(volume)
        self.datestr = date

    def get_full_date(self):
        return num2date(self.date)

    def get_date(self):
        return num2date(self.date).date()

    def get_date_num(self):
        return date2num(self.date)