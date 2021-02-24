import pytz
import datetime as dt


def curr_est_offset():
    """Calculate the current offset hours between UTC and EST (relative to daylight savings) using PyTZ"""
    tz_est = pytz.timezone('US/Eastern')
    offset = tz_est.utcoffset(dt.datetime.utcnow())
    offset_seconds = (offset.days * 86400) + offset.seconds
    offset_hours = offset_seconds // 3600
    return offset_hours  # -4 or -5


def orig_to_utc(dt_obj: dt.datetime, orig='EST'):
    """Convert a time from specified origin timezone to UTC"""
    return dt_obj + dt.timedelta(hours=-tz_map[orig])


def utc_to_dest(dt_obj: dt.datetime, dest='EST'):
    """Convert a time from UTC into a specified destination timezone"""
    return dt_obj + dt.timedelta(hours=tz_map[dest])


tz_map = {
    'UTC': 0,
    'EST': curr_est_offset(),
    'CST': curr_est_offset() - 1,
    'MST': curr_est_offset() - 2,
    'PST': curr_est_offset() - 3,
}

'''
a_time = dt.datetime.now()
a_time_2 = orig_to_utc(a_time)
print(a_time_2, dt.datetime.utcnow(), a_time.astimezone(pytz.utc))
print(utc_to_dest(a_time_2, 'PST'), a_time)
'''


def str_to_datetime(date_time_str):
    """
    Convert a string to a datetime object using different possible formats.

    First try '%Y-%m-%d %H:%M',
    then '%Y-%m-%d %H:%M:%S',
    before rasing a ValueError
    """
    try:  # Full datetime object (%Y-%m-%d %H:%M)
        return dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
    except ValueError:
        pass
    try:  # Full datetime object (%Y-%m-%d %H:%M:%S)
        return dt.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Invalid input
        raise ValueError(f'Invalid time input {date_time_str}. Read the docstring.')
