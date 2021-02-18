import datetime as dt


class Note:
    def __init__(self, userid: str, data: str):
        self._userid = userid
        self._data = data
        self._time_stamp = dt.datetime.now()

    def __repr__(self):
        return f"Note " \
           f"[ {self._data} " \
           f"| Created at {self.time_stamp} ]"

    @property
    def userid(self):
        return self._userid

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        if not new_data.strip():
            return
        self._data = new_data

    @property
    def time_stamp(self):
        return self._time_stamp


