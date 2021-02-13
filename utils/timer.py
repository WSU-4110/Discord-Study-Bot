import datetime as dt
import time
from datetime import timedelta as td


class Timer:
    def __init__(self, userid: str, initial_time: int, msg: str):
        self.userid = userid
        self.start_time = dt.datetime.now()
        self.end_time = self.start_time + td(minutes=initial_time)
        self.msg = msg

    def time_remaining(self):
        time.sleep(5)
        return self.end_time - dt.datetime.now()

    def __repr__(self):
        return f"Timer (User: {self.userid}) [ {self.end_time} | \"{self.msg}\" | Created at {self.start_time} | With " \
               f"{self.time_remaining()} time remaining]"

    def embed_repr(self):
        pass


t = Timer('12345', 1, 'Hello')
print(t)
