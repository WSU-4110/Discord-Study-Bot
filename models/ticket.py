from models import base_db_model
from typing import *


class Ticket(base_db_model.BaseDBModel):
    def __init__(self, userid: int, channelid: int, question: str, roles: List[str]):
        """ Initialize attributes of Ticket instance. """

        self._userid = userid
        self._channelid = channelid
        self._question = question
        self._roles = roles

    @property
    def userid(self):
        """ ID of user requesting Ticket creation. """
        return self._userid

    @property
    def channelid(self):
        """ ID of channel associated with the ticket. """
        return self._channelid

    @property
    def question(self):
        """ Message text associated with the ticket. """
        return self._question

    @property
    def roles(self):
        """ User roles desired when creating the ticket. """
        return self._roles.copy()
