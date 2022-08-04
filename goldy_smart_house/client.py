import goldy_smart_house
import devgoldyutils

import asyncio

MODULE_NAME = "CLIENT"

gsh_event_loop = asyncio.get_event_loop()

class Client(devgoldyutils.Console):
    """The Goldy Smart House client itself.
    
    Parameters
    ----------
    `method` : GSHMethod
        Enter the method you would like to use. You may chose one of the methods located in the ``goldy_smart_house.methods`` module.
        (E.g. `Dropbox()` )

    `google_nest_speaker_ip` : str
        Enter the IPv4 address of your Google Home device to ALLOW read backs. (Only works on Google Home Speakers)
        (E.g. `192.168.1.75` )

    `enable_logs` : bool
        Setting this to True enables all console info. Great for debuging.

    `read_back_volume` : int
        Allows you to adjust the smart speaker read back volume. (`0 - 100`)
        (E.g `20` )

    `string_match_fallback` : bool
        Allows you disable/enable string matching fallback.
    """
    def __init__(self, method:goldy_smart_house.methods.GSHMethod, google_nest_speaker_ip:str=None, enable_logs:bool=False, read_back_volume:int=None, string_match_fallback:bool=True):
        self.method_ = method
        self.google_nest_speaker_ip = google_nest_speaker_ip
        self.enable_logs = enable_logs
        self.read_back_volume = read_back_volume
        self.string_match_fallback = string_match_fallback

        self.google_nest_device = None
        if not google_nest_speaker_ip == None:
            self.google_nest_device = goldy_smart_house.google_nest_controller.GoogleNestDevice(ip=google_nest_speaker_ip, default_volume=self.read_back_volume)

        self.log = goldy_smart_house.utility.log
        
        # on_command Event Loop
        self.on_command_event_loop = goldy_smart_house.commands.Loop(self)

        super().__init__()

    @property
    def method(self):
        """Returns the method object of the method currently being used."""
        return self.method_

    def start(self):
        """Spins up the client and starts listening for commands on chosen method."""
        self.log(self, f"[{MODULE_NAME}] Client is starting up using the '{self.method.name}' method...")
        
        try:
            self.log(self, f"[{MODULE_NAME}] Client is Ready!")

            gsh_event_loop.run_until_complete(self.on_command_event_loop.run())
        except KeyboardInterrupt:
            self.on_command_event_loop.stop()

    def stop(self):
        """Stops the client from listenting/ends all loops."""
        self.log(self, f"[{MODULE_NAME}] {self.RED('Stopping Client!')}")
        self.on_command_event_loop.stop()