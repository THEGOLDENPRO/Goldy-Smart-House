from __future__ import annotations
import datetime

class Command(object):
    """A class representing a GSH command."""
    def __init__(self, id:int|None, command_string:str, date:datetime.datetime):
        self.id_ = id
        self.command_string_ = command_string
        self.date_ = date

    @property
    def id(self):
        """Some sort of unique identifier for this command."""
        return self.id_

    @property
    def command_string(self):
        """The command itself, what does it say."""
        return self.command_string_

    @property
    def datetime(self) -> datetime.datetime:
        """Python datetime object of when the command was executed."""
        return self.date_

    name = command_string