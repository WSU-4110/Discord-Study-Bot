import datetime as dt
import time
from datetime import timedelta as td


class Timer:
    def __init__(self, userid: str, initial_time: int, msg: str):
        self._userid = userid
        self.start_time = dt.datetime.now()
        self.end_time = self.start_time + td(minutes=initial_time)
        self.msg = msg

    def __repr__(self):
        return f"Timer (User: {self.userid}) [ {self.end_time} | \"{self.msg}\" | Created at {self.start_time} | With " \
               f"{self.time_remaining()} time remaining]"

    @property
    def userid(self):
        return self._userid

    def time_remaining(self):
        return self.end_time - dt.datetime.now()

    def embed_repr(self):
        pass

    def __lt__(self, obj):
        """self < obj."""
        return self.end_time < obj.end_time

    def __gt__(self, obj):
        """self > obj."""
        return self.end_time > obj.end_time

    def __cmp__(self, other):
        if self > other:
            return 1
        if self < other:
            return -1
        return 0
