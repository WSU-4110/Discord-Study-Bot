from utils import time_utils, config
from models import timer
from datetime import timedelta as td
import datetime as dt
import discord
import pytz

_days_abbr = ['m', 't', 'w', 'th', 'f', 's', 'su']


class Reminder(timer.Timer):
    # The init method has parameters all set to default values. This allows the builder to modify it later.
    def __init__(self, userid: str = None, msg: str = None, discord_message=None, day: str = None, hour: int = 0,
                 minute: int = 0,
                 recurring_type: int = 0, tz='EST'):
        """Constructor sets up attributes and prepares deadline"""
        self._today = dt.datetime.now()
        self._current_year = self._today.year
        self._hour = hour
        self._minute = minute
        self._next_date = self.get_next_reminder_date(day)
        self._day = self._next_date.day
        self._month = self._next_date.month
        self._tz = tz
        self.recurrence = recurring_type

        #  creates reminder notification time object
        deadline_date = time_utils.orig_to_utc(
            dt.datetime(self._current_year, self._month, self._day, self._hour, self._minute), orig=tz)

        # convert deadline_date to minutes
        seconds = (deadline_date - time_utils.orig_to_utc(self._today)).total_seconds()

        super().__init__(userid, seconds, msg, discord_message, include_seconds=True)

    # Setters for builder class. In python, @property is used to prohibit the method from being modified
    @property
    def set_hour(self, set_hour: int):
        self._hour = set_hour

    @property
    def set_min(self, set_min: int):
        self._minute = set_min

    @property
    def set_day(self, set_day: str):
        self._day = set_day

    @property
    def set_recurrence(self, set_recurrence: int):
        self.recurrence = set_recurrence

    @property
    def set_msg(self, msg: str):
        self._msg = msg



    # function methods below
    def get_next_reminder_date(self, day):
        """calculates the reminder date from day of week"""
        day_to_i = {d: i for i, d in enumerate(_days_abbr)}
        day_of_week = day_to_i[day.lower()]

        next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=0)

        if next_date == self._today:
            if self._hour <= self._today.hour:
                if self._minute <= self._today.minute:
                    next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=1)
        elif next_date < self._today:
            next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=1)

        return next_date

    # helper methods below
    def __instantiate_next_instance_of_reminder(self, limited_repetitions: bool = False):
        """ Creates new instance of the object in priority queue & database (only for pre_flight_for_deletion) """
        reminder_obj = Reminder(self.userid, self._msg, self._discord_message,
                                _days_abbr[self._next_date.weekday()], self._hour, self._minute,
                                (self.recurrence - (-1 if limited_repetitions else 0)), self._tz)
        config.timer_pqueue.add_task(reminder_obj)

        # reminder_obj.update(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'], self.message_id)
        reminder_obj.update(['start_time', 'end_time', 'msg', 'recurrence'], self.message_id)

        # override methods below

    def pre_flight_for_deletion(self):
        """ override for pre-flight check function to ensure if deletion (of a specific instance) should be allowed """
        if self.recurrence == 0:  # one-time reminder (default)
            return True
        elif self.recurrence <= -1:  # infinite reminder
            self.__instantiate_next_instance_of_reminder()
            return False
        elif self.recurrence > 0:  # reminder repeats limited number of times
            self.__instantiate_next_instance_of_reminder(True)
            return False

    # def formatted_discord_message(self):
    #     """The message that is sent to the user on timer event"""
    #     return f"{self.discord_message.author.mention} Your reminder for {str(self.end_time)} has finished. " \
    #            f"'Here's your initial message: {self.msg}"

    def embed(self):
        return discord.Embed(
            title="Reminder!",
            description=self.msg,
            # colour=cfg.Colors.SUCCESS
        ).add_field(
            name="Next Occurrence",
            value=time_utils.utc_to_dest(self._next_date + td(days=7)).strftime("%c")
        )
