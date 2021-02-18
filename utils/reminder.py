from utils import timer
from datetime import timedelta as td
import datetime as dt
import pytz as tz


class Reminder(timer.Timer):
    def __init__(self, userid: str, msg: str, discord_message, day: str, hour: int, minute: int):
        EST = tz.timezone('EST')
        self._today = dt.datetime.now(EST)
        self._current_year = self._today.year
        self._hour = hour
        self._minute = minute
        self._next_date = self.get_next_reminder_date(day)
        self._day = self._next_date.day
        self._month = self._next_date.month

        #  creates reminder notification time object
        deadline_date = dt.datetime(self._current_year, self._month, self._day, self._hour, self._minute)
        minutes = (deadline_date - self._today).total_seconds() / 60  # convert deadline_date to minutes

        super().__init__(userid, minutes, msg, discord_message)

    def get_next_reminder_date(self, day):
        day = day.upper()
        if (day == "M"):
            day_of_week = 0
        elif (day == "T"):
            day_of_week = 1
        elif (day == "W"):
            day_of_week = 2
        elif (day == "TH"):
            day_of_week = 3
        elif (day == "F"):
            day_of_week = 4
        elif (day == "SAT"):
            day_of_week = 5
        elif (day == "SUN"):
            day_of_week = 6

        next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=0)

        if next_date < self._today:
            next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=1)

        return next_date

    def formatted_discord_message(self):
        return f"{self.discord_message.author.mention} Your reminder for {str(self.end_time)} has finished. " \
               f"'Here's your initial message: {self.msg}"