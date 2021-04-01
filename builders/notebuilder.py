from abc import abstractmethod, ABC
from models.note import Note


class NoteBuilder(ABC):
    """ This is the builder interface which declares product construction steps"""
    @property
    def note(self):
        pass

    @property
    def __repr__(self):
        """ Function to represent object as string"""
        pass

    @staticmethod
    @abstractmethod
    def set_data(self, new_data):
        """ Function to add new note """
        pass

    @staticmethod
    @abstractmethod
    def get_data():
        """ Function returns the note """
        pass

    @staticmethod
    @abstractmethod
    def get_time_stamp(self):
        """ Function to return message time stamp """
        pass

    @staticmethod
    @abstractmethod
    def get_message_id(self):
        """ Function returns the message_id """
        pass


class PreBuiltNote(NoteBuilder, ABC):
    """ This is the concrete builder, it follows the builder interface and provides specific implementations of
    the building steps """
    def __init__(self):
        self.build_note = Note()

    def set_data(self, new_data):
        self.build_note.set_data("Calculus HW due friday!")
        return self




