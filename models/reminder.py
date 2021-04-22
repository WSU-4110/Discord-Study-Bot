from utils import time_utils, config, timer_priority_queue
from models import timer
from datetime import timedelta as td
import datetime as dt
import discord
import pytz

""" enum compares user input to python weekday format """
_days_abbr = ['m', 't', 'w', 'th', 'f', 's', 'su']

""" This class creates and instantiates a reminder object """


class Reminder(timer.Timer):
    def __init__(self, userid: str, msg: str, discord_message, day: str, hour: int, minute: int,
                 recurring_type: int = 0, tz='EST', roles=''):
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
        self.roles = ''

        # for loop parses roles from input if any exist
        starting_role_idx = 0
        for ele in msg.split(' '):
            if '<@&' in ele and '>' in ele:
                self.roles += ele + ' '
            else:
                starting_role_idx += 1
        self.roles = self.roles.strip()
        msg = ' '.join(msg.split(' ')[:starting_role_idx])

        # Creates reminder notification time object
        deadline_date = time_utils.orig_to_utc(
            dt.datetime(self._current_year, self._month, self._day, self._hour, self._minute), orig=tz)

        # Seconds information on object is converted to minutes
        seconds = (deadline_date - time_utils.orig_to_utc(self._today)).total_seconds()

        super().__init__(userid, seconds, msg, discord_message, include_seconds=True)

    # Creates a future date for same hour/minutes 7 days into the future
    def get_next_reminder_date(self, day):
        """calculates the reminder date from day of week"""
        day_to_i = {d: i for i, d in enumerate(_days_abbr)}
        day_of_week = day_to_i[day.lower()]

        next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=0)

        # Check if reminder occurs during current week or next week
        if next_date == self._today:
            if self._hour <= self._today.hour:
                if self._minute <= self._today.minute:
                    next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=1)
        elif next_date < self._today:
            next_date = self._today + td(days=-self._today.weekday() + day_of_week, weeks=1)

        return next_date

    # Method creates new reminder object and re-inserts into queue
    def __instantiate_next_instance_of_reminder(self, limited_repetitions: bool = False):
        """ Creates new instance of the object in priority queue & database (only for pre_flight_for_deletion) """
        reminder_obj = Reminder(self.userid, self._msg, self._discord_message,
                                _days_abbr[self._next_date.weekday()], self._hour, self._minute,
                                (self.recurrence - (-1 if limited_repetitions else 0)), self._tz)
        timer_priority_queue.TimerPriorityQueue.get_instance().add_task(reminder_obj)

        # reminder_obj.update(['message_id', 'userid', 'channel_id', 'start_time', 'end_time', 'msg', 'recurrence'], self.message_id)
        reminder_obj.update(['start_time', 'end_time', 'msg', 'recurrence', 'roles'], self.message_id)

        # override methods below

    def pre_flight_for_deletion(self):
        """override for pre-flight check function to ensure if deletion (of a specific instance) should be allowed"""
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
    # Embed formats Reminder alerts to look more professional
    def embed(self):
        return discord.Embed(
            title="Reminder!",
            description=self.msg,
            # colour=cfg.Colors.SUCCESS
        ).add_field(
            name="Next Occurrence",
            value=time_utils.utc_to_dest(self._next_date + td(days=7)).strftime("%c")
        )
