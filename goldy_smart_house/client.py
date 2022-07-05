import goldy_smart_house
import asyncio

MODULE_NAME = "CLIENT"

gsh_event_loop = asyncio.get_event_loop()

class Client():
    """The Goldy Smart House client itself.
    
    Parameters
    ----------
    `dropbox_share_link` : str
        Copy and enter the share link to the commands.txt file from your Dropbox.
        (E.g. `https://www.dropbox.com/s/g4iqud3t37jvlk8/sus%20-%202022.txt`)

    `google_nest_speaker_ip` : str
        Enter the IPv4 address of your Google Home device to ALLOW read backs. (Only works on Google Home Speakers)
        (E.g. `192.168.1.75`)

    `enable_logs` : bool
        Setting this to True enables all console info. Great for debuging.

    `read_back_volume` : int
        Allows you to adjust the smart speaker read back volume. (`0 - 100`)
        (E.g `20`)
    """
    def __init__(self, dropbox_share_link:str, google_nest_speaker_ip:str=None, enable_logs:bool=False, read_back_volume:int=None):
        self.dropbox_share_link = dropbox_share_link
        self.google_nest_speaker_ip = google_nest_speaker_ip
        self.enable_logs = enable_logs
        self.read_back_volume = read_back_volume

        self.dropbox = goldy_smart_house.dropbox.Dropbox(self.dropbox_share_link)
        self.google_nest_device = None
        if not google_nest_speaker_ip == None:
            self.google_nest_device = goldy_smart_house.google_nest_controller.GoogleNestDevice(ip=google_nest_speaker_ip, default_volume=self.read_back_volume)

        self.log = goldy_smart_house.utility.log
        
        # on_command Event Loop
        self.on_command_event_loop = goldy_smart_house.commands.Loop(self)

    def start(self):
        """Spins up the client and starts listening commands."""
        self.log(self, f"[{MODULE_NAME}] Client is starting up...")
        
        try:
            gsh_event_loop.run_until_complete(self.on_command_event_loop.run())
        except KeyboardInterrupt:
            self.on_command_event_loop.stop()

        self.log(self, f"[{MODULE_NAME}] Client is Ready!")

    def stop(self):
        """Stops the client from listenting/ends all loops."""
        self.on_command_event_loop.stop()