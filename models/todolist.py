import datetime as dt
from models import base_db_model


class ToDoList():
    def __init__(self, userid: str, td_secs: int, msg: str, discord_message, start_time: dt.datetime = dt.datetime.utcnow(), end_time=None):
        """ Default constructor """
        self._userid = userid
        self._msg = msg  # remaining message text
        self._discord_message = discord_message  # message object
        self.message_id = self._discord_message.id
        self.channel_id = self._discord_message.channel.id
        if end_time is None:
            self._end_time = start_time + dt.timedelta(seconds=td_secs)
        else:
            self._end_time = end_time
        self._start_time = start_time

    def __repr__(self):
        """ Function to represent object as string"""
        return f"To Do Item " \
               f"[ {self._msg} " \
               f"| Created at {self.start_time} ]"

    def get_message_id(self):
        """ Function returns the message_id """
        return self.message_id

    def get_msg(self):
        """ Function returns the msg """
        return self._msg
    
    @property
    def end_time(self):
        """ Function returns the end_time """
        return self._end_time

    @property
    def userid(self):
        """ Function to return the userid """
        return self._userid

    @property
    def msg(self):
        """ Function to return the message entered by user """
        return self._msg

    @msg.setter
    def msg(self, new_msg):
        """ Function to add new message """
        if not new_msg.strip():
            return
        self._msg = new_msg

    @property
    def start_time(self):
        """ Function to return message time stamp """
        return self._start_time

    @property
    def discord_message(self):
        """ Message object from Timer creation request. """
        return self._discord_message
    
    def formatted_discord_message(self):
        """ Returns message sent when Timer instance is activated. """

        return f"Alerting{self.discord_message.author.mention}!"

    def time_remaining(self):
        """ Returns remaining time until Timer activation. """

        return self.end_time - dt.datetime.utcnow()
    
    # COMPARISON FUNCTIONS
    
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
