import ctypes
import threading
import time
import goldy_smart_house
import datetime

class Command(object):
    """Formats a plain unformatted command in commands.txt into a command class object."""
    def __init__(self, unformatted_command_string:str):
        self.unformatted_command_string = unformatted_command_string

    @property
    def id(self):
        return self.command_id

    @property
    def name(self):
        return self.unformatted_command_string.split("]: ", 2)[1]

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.unformatted_command_string.split(": ")[0], "[%B %d, %Y at %I:%M%p]")

class Loop(threading.Thread):
    """'on_command' event Loop."""
    def __init__(self, dropbox:goldy_smart_house.dropbox.Dropbox):
        threading.Thread.__init__(self)
        self.stop_ = False

        self.dropbox = dropbox
        
    def run(self):
        # Append all old commands to cache.
        for line in self.dropbox.read_file().splitlines():
            goldy_smart_house.cache.main_cache_dict["old_commands"].append(line)
        
        
        while True:
            command_list = self.dropbox.read_file().splitlines()

            # This triggers when a new command is found in 'commands.txt'.
            if len(command_list) > len(goldy_smart_house.cache.main_cache_dict["old_commands"]):

                # Checks if the command has been declared in user's code.
                result = self.does_command_exist(Command(command_list[-1]))
                if result[0]:
                    # Runs the Function
                    goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{result[1]}"]["function_object"]()

                goldy_smart_house.cache.main_cache_dict["old_commands"].append(line)

            time.sleep(1)

            if self.stop_:
                break

    def stop(self):
        self.stop_ = True

    def does_command_exist(self, command:Command) -> tuple:
        """Checks if the command exists."""
        for assigned_command in goldy_smart_house.cache.main_cache_dict["assigned_commands"]:
            if (command.name).lower() == goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["name"]:
                return (True, assigned_command)
            
        return (False, None)

    def has_command_been_ran_already(self, command:Command) -> bool:
        if command.id in goldy_smart_house.cache.main_cache_dict["commands_ran"]:
            return True

        return False