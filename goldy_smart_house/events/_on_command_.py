from .. import cache
from typing import List

def on_command(command_name:str=None, smart_speaker_read_backs:bool=True, alias_names:List[str]=[]):
    """Runs whenever a command is called by the smart speaker.

    Parameters
    ----------
    `command_name` : str
        The actual name the smart speaker will recognise the command as.

    `smart_speaker_read_backs` : bool
        Allows you to return strings that your smart speaker will read out. (Only works on Google Home Speakers and IPv4 of the device will be needed.)

    `alias_names` : List[str]
        Allows you to give the command different trigger names that it can fallback on incase the output from the smart speaker isn't as expected. (THE MORE, THE BETTER!)
    """

    def inner(func, command_name=None, smart_speaker_read_backs:bool=True, alias_names:List[str]=[]):
        # Store command in cache.
        if command_name == None:
            command_name = func.__name__
        
        cache.main_cache_dict["assigned_commands"][f"{command_name}".replace(" ", "_")] = {
                "name": f"{command_name}".replace("_", " "),
                "code_name": f"{command_name}".replace(" ", "_"),
                "alias_names":alias_names,
                "smart_speaker_read_back": smart_speaker_read_backs,
                "function_object": func
            }

    return inner