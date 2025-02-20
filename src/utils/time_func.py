from datetime import datetime, timedelta
import pytz


def get_current_time(strftime = True):
    timezone = pytz.timezone('Asia/Kolkata')
    time = datetime.now(tz=timezone)
    if strftime:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    
    return time


def set_exp_time(strftime = True):
    timezone = pytz.timezone("Asia/Kolkata")
    time = datetime.now(tz=timezone)
    newtime = time + timedelta(minutes=2)
    
    if strftime:
        return newtime.strftime("%Y-%m-%d %H:%M:%S")
    
    return newtime