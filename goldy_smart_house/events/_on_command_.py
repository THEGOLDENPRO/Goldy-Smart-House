from .. import cache

def on_command(command_name:str=None, smart_speaker_read_backs:bool=True):
    """Runs whenever a command is called by the smart speaker.

    Parameters
    ----------
    `command_name` : str
        The actual name the smart speaker will recognise the command as.

    `smart_speaker_read_backs` : bool
        Allows you to return strings that your smart speaker will read out. (Only works on Google Home Speakers and IPv4 of the device will be needed.)
    """

    def inner(func, command_name=None, smart_speaker_read_backs:bool=True):
        # Store function in cache.
        if command_name == None:
            command_name = func.__name__
        
        cache.main_cache_dict["assigned_commands"][f"{command_name}"] = {
                "name": f"{command_name}".replace("_", " "),
                "code_name": f"{command_name}",
                "smart_speaker_read_back": smart_speaker_read_backs,
                "function_object": func
            }

    return inner