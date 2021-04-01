from abc import abstractmethod
from models.reminder import Reminder

#This specifies methods for creating reminders
class ReminderBuilder():

    @property
    def reminder(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def set_day(self):
        pass

    @staticmethod
    @abstractmethod
    def set_hour(self):
        pass

    @staticmethod
    @abstractmethod
    def set_minute(self):
        pass

    @staticmethod
    @abstractmethod
    def set_recurrence(self):
        pass

    @staticmethod
    @abstractmethod
    def get_reminder():
        pass

#The concrete builder that provide specific implementation of abstract methods in Reminder Builder
#This class sets the needed parameters to properly build a reminder
class PreBuiltReminderMon(ReminderBuilder):

    def __init__(self):
        self.build_reminder = Reminder()

    def set_day(self):
        self.build_reminder.set_day('m')
        return self

    def set_hour(self):
        self.build_reminder.set_hour(17)
        return self

    def set_minute(self):
        self.build_reminder.set_min(30)
        return self

    def set_recurrence(self):
        self.build_reminder.set_recurrence(-1)
        return self

    def get_reminder(self):
        return self.build_reminder
