# Goldy Smart House *(A Python Google Home Module)*

![Discord Shield](https://discordapp.com/api/guilds/759051039470387272/widget.png?style=shield)

<p align="center">
 <img src="https://media.discordapp.net/attachments/436201641486581762/959065479056601128/Untitled-1.png" width="800" />
</p>

### ``Goldy Smart House`` - A shity python module that allows a Google Assistant device (Google Home, etc) to run code on your computer.

# *WARNING*
Before I explain anything further, I would like to say that I made this module just for a **[YouTube Video](https://youtu.be/_bkefjTpagA)**, hence it wasn't a good implementation, I just did it for fun and entertainment but with all that aside you can use the module for whatever you like and you can maybe even fork it to perhaps improve the library. I Just don't want to see comments like "this was a sh#t implementation" or "the code is bad".

# *What is Goldy Smart House?*
Goldy Smart House is a python module that allows a Google Assistant device (Google Home, etc) to run code on your computer. 

The Libary allows your google assistant to run commands/functions in your code and also allows you to return a string back to a device like the google home if included IP address of the device which was assigned by your router.

Just made this for a **[YouTube Video](https://youtu.be/_bkefjTpagA)** but I might actually update it and fix my code in the future.

## *Install/Set Up*
1. **Install package from pip.**
```sh
#Windows/Linux

pip install goldysmarthouse
```
2. **That's It!** 
```python
from goldy_smart_house import events, Client

client = Client("[dropbox_share_link]", google_nest_speaker_ip="[e.g. 192.168.1.75]", enable_logs=True, read_back_volume=11)

@events.on_command()
def open_notepad():
    subprocess.Popen(["C:/Windows/System32/notepad.exe"]) # This only works on windows.
    return "Notepad open"

client.start()
```

###### **[[YouTube Video]](https://youtu.be/_bkefjTpagA)** (PYPI: [INSTALL HERE](https://pypi.org/project/goldysmarthouse/))
