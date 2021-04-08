import datetime as dt
from datetime import timedelta as td
import discord
from models import base_db_model, note
from utils import time_utils, database_utils
from typing import *


class Ticket(base_db_model.BaseDBModel):
    def __init__(self, userid: int, channelid: int, question: str, roles: List[str]):
        self._userid = userid
        self._channelid = channelid
        self._question = question
        self._roles = roles
        self._resolved = False

    @property
    def userid(self):
        return self._userid

    @property
    def channelid(self):
        return self._channelid

    @property
    def question(self):
        return self._question

    @property
    def roles(self):
        return self._roles.copy()

    @property
    def resolved(self):
        return self._resolved

    def resolve(self):
        self._resolved = True
