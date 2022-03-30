import threading
import time
import goldy_smart_house
import datetime
import asyncio

MODULE_NAME = "COMMANDS"

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
    def __init__(self, client:goldy_smart_house.client.Client):
        threading.Thread.__init__(self)
        self.stop_ = False

        self.client = client
        self.dropbox = client.dropbox
        self.log = goldy_smart_house.utility.log
        
    def run(self):
        # Append all old commands to cache.
        for line in self.dropbox.read_file().splitlines():
            goldy_smart_house.cache.main_cache_dict["old_commands"].append(line)
        
        
        while True:
            command_list = self.dropbox.read_file().splitlines()

            # This triggers when a new command is found in 'commands.txt'.
            if len(command_list) > len(goldy_smart_house.cache.main_cache_dict["old_commands"]):
                new_command = Command(command_list[-1])
                self.log(self.client, f"[{MODULE_NAME}] NEW command detected >>> {new_command.name}")

                # Checks if the command has been declared in user's code.
                result = self.does_command_exist(new_command)
                if result[0]:
                    self.log(self.client, f"[{MODULE_NAME}] Command found, running it's function...")
                    # Runs the Function
                    self.execute_command_func(
                        func=goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{result[1]}"]["function_object"], 
                        result=result)

                else:
                    self.log(self.client, f"[{MODULE_NAME}] That command was not found!")

                goldy_smart_house.cache.main_cache_dict["old_commands"].append(line)

            time.sleep(1)

            if self.stop_:
                self.log(self.client, f"[{MODULE_NAME}] Loop stopped!")
                break

    def stop(self):
        self.stop_ = True

    def execute_command_func(self, func, result):
        read_back_string = func()
        self.log(self.client, f"[{MODULE_NAME}] Function executed!")
        if goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{result[1]}"]["smart_speaker_read_back"]:
            if not read_back_string == None:
                if not self.client.google_nest_device == None:
                    self.log(self.client, f"[{MODULE_NAME}] Reading back to Google Nest Device...")
                    self.client.google_nest_device.say(read_back_string)

    def does_command_exist(self, command:Command) -> tuple:
        """Checks if the command exists."""
        for assigned_command in goldy_smart_house.cache.main_cache_dict["assigned_commands"]:
            if (command.name).lower() == goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["name"]:
                return (True, assigned_command)
            
        return (False, None)