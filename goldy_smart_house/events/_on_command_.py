from .. import cache

def on_command(func, command_name:str=None, return_to_smart_speaker:bool=True):
    """Runs whenever a command is called by the smart speaker.

    Parameters
    ----------
    `command_name` : str
        The actual name the smart speaker will recognise the command as.

    `return_to_smart_speaker` : bool
        Allows you to return strings that your smart speaker will read out. (Only works on Google Home Speakers and IPv4 of the device will be needed.)
    """

    # Store function in cache.
    if command_name == None:
        command_name = func.__name__
    
    cache.main_cache_dict["assigned_commands"][f"{command_name}"] = {
            "name": f"{command_name}".replace("_", " "),
            "code_name": f"{command_name}",
            "return_to_smart_speaker": return_to_smart_speaker,
            "function_object": func
        }

    print(cache.main_cache_dict)