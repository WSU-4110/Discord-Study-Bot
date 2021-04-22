import datetime as dt
from datetime import timedelta as td
from models import base_db_model
from utils import time_utils, database_utils
import discord


class Timer(base_db_model.BaseDBModel):
    def __init__(self, userid: str, td_secs: int, msg: str, discord_message, include_seconds=True, start_time=None,
                 end_time=None):
        """ Initialize attributes of Timer instance. """

        self._userid = userid
        if start_time is None and end_time is None:
            self._start_time = dt.datetime.utcnow()  # UTC time standard
            self._end_time = self.start_time + td(seconds=td_secs)
        else:
            self._start_time = start_time
            self._end_time = end_time
        if not include_seconds:
            self._start_time = time_utils.str_to_datetime(self._start_time.strftime("%Y-%m-%d %H:%M"))
            self._end_time = time_utils.str_to_datetime(self._end_time.strftime("%Y-%m-%d %H:%M"))
        self._msg = msg  # remaining message text
        self._discord_message = discord_message  # message object
        if self._discord_message is not None:
            self._message_id = self._discord_message.id
            self._channel_id = self._discord_message.channel.id
        else:
            self._channel_id = self._message_id = 0

    def __repr__(self):
        """ Get string representation of Timer instance information. """

        return f"Timer (User: {self.userid}) " \
               f"[ {self.end_time} | \"{self.msg}\" " \
               f"| Created at {self.start_time} " \
               f"| With {self.time_remaining()} time remaining ]"

    # ----- PROPERTIES ----- #

    @property
    def userid(self):
        """ ID of user requesting Timer creation. """
        return self._userid

    @property
    def start_time(self):
        """ Time of Timer creation. """
        return self._start_time

    @property
    def end_time(self):
        """ Timer activation datetime. """
        return self._end_time

    @property
    def msg(self):
        """ Message text associated with Timer instance. """
        return self._msg

    @msg.setter
    def msg(self, new_msg):
        self._msg = new_msg

    @property
    def discord_message(self):
        """ Message object from Timer creation request. """
        return self._discord_message

    @property
    def message_id(self):
        """ ID of Message object. """
        return self._message_id

    @property
    def channel_id(self):
        """ ID of Message object. """
        return self._channel_id

    # ----- #

    def formatted_discord_message(self):
        """ Returns message sent when Timer instance is activated. """

        return f"Alerting {self.discord_message.author.mention}!"

    def time_remaining(self):
        """ Returns remaining time until Timer activation. """

        return self.end_time - dt.datetime.utcnow()

    def embed(self):
        """ Returns Discord Embed representation for message sent when Timer instance is activated. """

        return discord.Embed(
            title="Timer Expired!",
            description=self.msg,
            # colour=cfg.Colors.SUCCESS
        )

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
