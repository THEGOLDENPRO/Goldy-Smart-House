from __future__ import annotations
import asyncio
import requests
import datetime

import goldy_smart_house
import devgoldyutils
from . import GSHMethod

event_loop = asyncio.get_event_loop()

class Dropbox(GSHMethod):
    """The Dropbox method."""

    def __init__(self, share_link:str) -> None:
        self.share_link = self.validate_link(share_link)
        super().__init__(name="Dropbox")

        self.connection_session = requests.Session()

        # Append all old commands to cache.
        for line in self.read_file().splitlines():
            goldy_smart_house.cache.main_cache_dict["old_commands"].append(self.convert_string_to_command(line))

    async def has_command_triggered(self) -> goldy_smart_house.objects.Command|None:
        command_list = await self.read_file_async()
        command_list = command_list.splitlines()

        # This triggers when a new command is found in 'commands.txt'.
        if len(command_list) > len(goldy_smart_house.cache.main_cache_dict["old_commands"]):
            new_command = self.convert_string_to_command(command_list[-1])

            goldy_smart_house.cache.main_cache_dict["old_commands"].append(new_command)

            return new_command

        return None

    def convert_string_to_command(self, command_string:str):
        return goldy_smart_house.objects.Command(id=None, 
            command_string=command_string.split("]: ", 2)[1], 
            date=datetime.datetime.strptime(command_string.split(": ")[0], "[%B %d, %Y at %I:%M%p]"))

    async def read_file_async(self):
        return self.connection_session.get(self.share_link).text

    def read_file(self):
        return self.connection_session.get(self.share_link).text

    def validate_link(self, share_link:str) -> str:
        """Tries to return a correctly formated dropbox link."""
        
        if share_link[-1:] == "?":
            return share_link + "dl=1"

        if not share_link[-5:] in ["?dl=1", "?dl=0"]:
            return share_link + "?dl=1"

        if share_link[-5:] == "?dl=0":
            return share_link[:-5] + "?dl=1"