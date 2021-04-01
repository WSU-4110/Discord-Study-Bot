from builders import notebuilder


class NoteDirector:
    """ The director is responsible for executing the building steps in a particular sequence"""
    def __init__(self):
        self._builder = None

    """ This is where we implement the classes from the interface"""
    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder: notebuilder):
        self._builder = builder

    def build_note(self, data):
        self.builder.set_data(data)

    def get_note(self):
        self.builder.get_data()

    def get_time_stamp(self):
        self._builder.get_time_stamp()

    def get_message_id(self):
        self._builder.get_message_id()
