import threading
import time
from thefuzz import process, fuzz

import goldy_smart_house
import devgoldyutils


MODULE_NAME = "COMMANDS"

class Loop(threading.Thread):
    """'on_command' event Loop."""
    def __init__(self, client:goldy_smart_house.client.Client):
        threading.Thread.__init__(self)
        self.stop_ = False

        self.client = client
        self.log = goldy_smart_house.utility.log
        
    async def run(self):
        self.log(self.client, f"[{MODULE_NAME}] {self.client.GREEN('Listening for commands...')}")
        
        while True:
            new_command = await self.client.method.has_command_triggered()

            if not new_command == None:
                self.log(self.client, f"[{MODULE_NAME}] NEW command detected >>> {self.client.BLUE(new_command.name)}")

                # Checks if the command has been declared in user's code.
                result = self.does_command_exist(new_command)
                if result[0]:
                    self.log(self.client, f"[{MODULE_NAME}] Command found, running it's function...")
                    # Runs the Function
                    await self.execute_command_func(
                        func=goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{result[1]}"]["function_object"], 
                        command_name=result[1])

                else:
                    self.log(self.client, f"[{MODULE_NAME}] That command was not found!")

            time.sleep(0.2)

            if self.stop_:
                self.log(self.client, f"[{MODULE_NAME}] Loop stopped!")
                break

    def stop(self):
        self.stop_ = True

    async def execute_command_func(self, func, command_name:str):
        read_back_string = await func()
        self.log(self.client, f"[{MODULE_NAME}] {self.client.GREEN('Function executed!')}")
        if goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{command_name}"]["smart_speaker_read_back"]:
            if not read_back_string == None:
                if not self.client.google_nest_device == None:
                    self.log(self.client, f"[{MODULE_NAME}] Reading back to Google Nest Device...")
                    self.client.google_nest_device.say(read_back_string)

    def does_command_exist(self, command:goldy_smart_house.objects.Command) -> tuple:
        """Checks if the command exists."""
        # Find assigned command with exact match.
        #-------------------------------------------
        for assigned_command in goldy_smart_house.cache.main_cache_dict["assigned_commands"]:
            if (command.name).lower() == goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["name"]:
                return (True, assigned_command)

            # Alias name support.
            if (command.name).lower() in goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["alias_names"]:
                pass

        # String Match Fallback - If the command detected isn't named exactly as it is on GSH, string match will try and find the right command.
        #--------------------------------------------------------------------------------------------------------------------------------------------
        if self.client.string_match_fallback:
            self.log(self.client, f"[{MODULE_NAME}] {self.client.PURPLE('Falling back on String Matching to find the command...')}")
            print(devgoldyutils.Console().PURPLE('Falling back on String Matching to find the command...'))

            for assigned_command in goldy_smart_house.cache.main_cache_dict["assigned_commands"]:

                # Creating list of all names this assigned command is under.
                assigned_command_names = [
                    goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["name"]
                ]
                for alias_name in goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["alias_names"]:
                    assigned_command_names.append(alias_name)

                # Do actual string matching.
                command_found = process.extractOne((command.name).lower(), choices=assigned_command_names, score_cutoff=85, scorer=fuzz.ratio)
                if not command_found == None:
                    return (True, assigned_command)
            
        return (False, None)