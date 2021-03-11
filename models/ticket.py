import datetime as dt
from datetime import timedelta as td
from models import base_db_model
from utils import time_utils, database_utils
from typing import *


class Ticket(base_db_model.BaseDBModel):
    def __init__(self, userid: str, channelid: str, msg: str, roles: List[str, ...]):
        pass
