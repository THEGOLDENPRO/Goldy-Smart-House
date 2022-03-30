import subprocess
from goldy_smart_house import events, Client, GoogleNestDevice
import webview
import novauniverse

client = Client("https://www.dropbox.com/s/ethmzb3v1mzjsw2/commands.txt?dl=0", google_nest_speaker_ip="192.168.1.75", enable_logs=True, read_back_volume=11)

@events.on_command()
def open_notepad():
    subprocess.Popen(["C:/Windows/System32/notepad.exe"])
    return "Notepad open"

@events.on_command()
def check_who_is_online_on_nova():
    online_players = []
    server = novauniverse.Server()
    
    for player in server.online_players:
        online_players.append(player.name)

    amount_of_online_players = len(online_players)
    
    if amount_of_online_players == 0:
        return "No one is online."

    if amount_of_online_players == 1:
        return f"{online_players[0]} is online."

    if amount_of_online_players > 1:
        sentence = ""
        count = 0
        for player in online_players:
            count += 1

            if not count == (amount_of_online_players - 1):
                sentence += f"{player}, "
            if count == (amount_of_online_players - 1):
                sentence += f"{player} and "
            if count == amount_of_online_players:
                sentence += f"{player}."

        return sentence

@events.on_command()
def stop_client():
    client.stop()

@events.on_command()
def test():
    webview.create_window('Rickroll', 
    html="<iframe width='100%' height='100%' src='https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1' frameborder='0' allowfullscreen></iframe>", 
    width=1200, height=680, min_size=(1200, 680), fullscreen=True)
    webview.start()

client.start()