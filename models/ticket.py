from models import base_db_model
from typing import *


class Ticket(base_db_model.BaseDBModel):
    def __init__(self, msg_id: int, user_id: int, channel_id: int, question: str, roles: List[str]):
        """ Initialize attributes of Ticket instance. """

        self._message_id = msg_id
        self._user_id = user_id
        self._channel_id = channel_id
        self._question = question
        self._roles = roles

    @property
    def message_id(self):
        """ ID of message requesting Ticket creation. """
        return self._message_id

    @property
    def user_id(self):
        """ ID of user requesting Ticket creation. """
        return self._user_id

    @property
    def channel_id(self):
        """ ID of channel associated with the ticket. """
        return self._channel_id

    @property
    def question(self):
        """ Message text associated with the ticket. """
        return self._question

    @property
    def roles(self):
        """ User roles desired when creating the ticket. """
        return self._roles.copy()
