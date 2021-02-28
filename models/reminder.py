from utils import timeutils
from models import timer
from datetime import timedelta as td
import datetime as dt
import pytz


class Reminder(timer.Timer):
    def __init__(self, userid: str, msg: str, discord_message, day: str, hour: int, minute: int, tz='EST'):
        """Constructor sets up attributes and prepares deadline"""
        self._today = dt.datetime.utcnow()
        self._current_year = self._today.year
        self._hour = hour
        self._minute = minute
        self._next_date = self.get_next_reminder_date(day)
        self._day = self._next_date.day
        self._month = self._next_date.month

        #  creates reminder notification time object
        deadline_date = timeutils.orig_to_utc(
            dt.datetime(self._current_year, self._month, self._day, self._hour, self._minute), orig=tz)
        minutes = (deadline_date - self._today).total_seconds() // 60  # convert deadline_date to minutes

        super().__init__(userid, minutes, msg, discord_message,True)

    def get_next_reminder_date(self, day):
        """calculates the reminder date from day of week"""
        day_to_i = {d: i for i, d in enumerate(['m', 't', 'w', 'th', 'f', 's', 'su'])}
        day_of_week = day_to_i[day.lower()]

        next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=0)

        if next_date < self._today:
            next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=1)

        return next_date

    def formatted_discord_message(self):
        """The message that is sent to the user on timer event"""
        return f"{self.discord_message.author.mention} Your reminder for {str(self.end_time)} has finished. " \
               f"'Here's your initial message: {self.msg}"
