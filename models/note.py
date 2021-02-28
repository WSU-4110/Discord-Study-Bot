import datetime as dt


class Note:

    def __init__(self, userid: str, data: str):
        """ Default constructor """
        self._userid = userid
        self._data = data
        self._time_stamp = dt.datetime.now()

    def __repr__(self):
        """ Function to represent object as string"""
        return f"Note " \
               f"[ {self._data} " \
               f"| Created at {self.time_stamp} ]"

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
