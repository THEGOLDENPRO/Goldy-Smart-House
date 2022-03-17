from goldy_smart_house import events, Client

client = Client("https://www.dropbox.com/s/ethmzb3v1mzjsw2/commands.txt?dl=0")

@events.on_command
def open_notepad():
    pass

@events.on_command
def stop_client():
    client.stop()

client.start()