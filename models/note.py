import datetime as dt
from models import base_db_model


class Note(base_db_model.BaseDBModel):
    def __init__(self, msg_id: int, userid: int, data: str, time_stamp: dt.datetime = dt.datetime.now()):
        """ Default constructor """
        self._message_id = msg_id
        self._userid = userid
        self._data = data
        self._time_stamp = time_stamp

    def __repr__(self):
        """ Function to represent object as string"""
        return f"Note " \
               f"[ {self._data} " \
               f"| Created at {self.time_stamp} ]"

    def get_message_id(self):
        """ Function returns the message_id """
        return self._message_id

    def get_data(self):
        """ Function returns the message_data """
        return self._data
    
    @property
    def userid(self):
        """ Function to return the userid """
        return self._userid

    @property
    def data(self):
        """ Function to return the message entered by user """
        return self._data

    @data.setter
    def data(self, new_data):
        """ Function to add new message """
        if not new_data.strip():
            return
        self._data = new_data

    @property
    def time_stamp(self):
        """ Function to return message time stamp """
        return self._time_stamp
