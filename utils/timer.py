import datetime as dt
from datetime import timedelta as td


class Timer:
    def __init__(self, userid: str, time_delta_mins: int, msg: str, discord_message):
        self._userid = userid
        self._start_time = dt.datetime.now()
        self._end_time = self.start_time + td(minutes=time_delta_mins)
        self._msg = msg
        self._discord_message = discord_message

    def __repr__(self):
        return f"Timer (User: {self.userid}) " \
               f"[ {self.end_time} | \"{self.msg}\" " \
               f"| Created at {self.start_time} " \
               f"| With {self.time_remaining()} time remaining ]"

    @property
    def userid(self):
        return self._userid

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, new_msg):
        self._msg = new_msg

    @property
    def discord_message(self):
        return self._discord_message

    def formatted_discord_message(self):
        return f"{self.discord_message.author.mention} Your timer for {str(self.end_time)} has finished. " \
               f"'Here's your initial message: {self.msg}"

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
