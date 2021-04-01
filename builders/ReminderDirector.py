from builders import ReminderBuilder


# This class executes the building steps needed to create the reminder.
# It can take in different builders and assemble the object according to that builder
class ReminderDirector:

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> ReminderBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ReminderBuilder) -> None:
        self._builder = builder

    def build_reminder(self) -> None:
        self.builder.set_day()
        self.builder.set_hour()
        self.builder.set_min()
        self.builder.set_recurrence()

    def get_reminder(self):
        self.builder.get_reminder()