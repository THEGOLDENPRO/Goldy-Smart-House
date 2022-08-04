"""
The module thats houses all the different methods.
"""
from __future__ import annotations

import goldy_smart_house

class GSHMethod(object):
    """The base class for all GSH methods."""

    def __init__(self, name:str) -> None:
        self.name_ = name
        
    @property
    def name(self) -> str:
        """Get name of this method."""
        return self.name_.upper()

    async def has_command_triggered(self) -> goldy_smart_house.objects.Command|None:
        """
        This method will be called by the ``on_command`` loop every second to check if a command has been triggered here. 
        GSH expects this to return a ``command object`` if a command has been triggered. 
        If no new command has been triggred it expects to return ``None``. 
        You'll have to handle this all by yourself accordingly to your method.
        """
        return None

    grab_command = has_command_triggered
    get_command = has_command_triggered

from .dropbox import Dropbox