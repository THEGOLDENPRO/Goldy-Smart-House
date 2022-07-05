import threading
import time
import goldy_smart_house

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
                        result=result)

                else:
                    self.log(self.client, f"[{MODULE_NAME}] That command was not found!")

            time.sleep(0.2)

            if self.stop_:
                self.log(self.client, f"[{MODULE_NAME}] Loop stopped!")
                break

    def stop(self):
        self.stop_ = True

    async def execute_command_func(self, func, result):
        read_back_string = await func()
        self.log(self.client, f"[{MODULE_NAME}] {self.client.GREEN('Function executed!')}")
        if goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{result[1]}"]["smart_speaker_read_back"]:
            if not read_back_string == None:
                if not self.client.google_nest_device == None:
                    self.log(self.client, f"[{MODULE_NAME}] Reading back to Google Nest Device...")
                    self.client.google_nest_device.say(read_back_string)

    def does_command_exist(self, command:goldy_smart_house.objects.Command) -> tuple:
        """Checks if the command exists."""
        for assigned_command in goldy_smart_house.cache.main_cache_dict["assigned_commands"]:
            if (command.name).lower() == goldy_smart_house.cache.main_cache_dict["assigned_commands"][f"{assigned_command}"]["name"]:
                return (True, assigned_command)
            
        return (False, None)