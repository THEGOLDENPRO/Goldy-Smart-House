import goldy_smart_house

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
    """
    def __init__(self, dropbox_share_link:str, google_nest_speaker_ip:str=None):
        self.dropbox_share_link = dropbox_share_link
        self.google_nest_speaker_ip = google_nest_speaker_ip
        
        # on_command Event Loop
        self.on_command_event_loop = goldy_smart_house.commands.Loop(goldy_smart_house.dropbox.Dropbox(self.dropbox_share_link))

    def start(self):
        """Spins up the client and starts listening for the smart speaker."""
        self.on_command_event_loop.run()

    def stop(self):
        """Stops the client from listenting/ends all loops."""
        self.on_command_event_loop.stop()