import time
import threading
import requests
from googlecontroller import GoogleAssistant as _GA_
import librosa
class GoogleNestDevice(_GA_):
    def __init__(self, ip, default_volume=18):
        self.ip = ip
        _GA_.__init__(self, ip)

        self.nest_device = _GA_(host=self.ip)

        if not default_volume == None:
            self.volume_num = default_volume
        else:
            self.volume_num = 18

    def play(self, url, ignore = False, contenttype = "audio/mp3"):
        if self.cc.media_controller.status.player_state != "PLAYING" or ignore == True:
            self.cc.wait()
            media = self.cc.media_controller
            media.play_media(url, contenttype)
            media.block_until_active()

    def say(self, text:str, ignore:bool=False, lang:str="en-UK"):
        volume_num = self.volume_num + 18
        self.volume(volume_num)

        speed = "1"
        url = u"https://translate.google.com/translate_tts?ie=UTF-8&q=" + text + "%21&tl=" + lang + "&ttsspeed=" + speed + "&total=1&idx=0&client=tw-ob&textlen=14&tk=594228.1040269"
        
        open("./temp.mp3", "wb").write(requests.get(url).content)
        threading.Thread(target=self.play, args=(url, False,)).start()

        self.block_until_done_playing(audio_length=librosa.get_duration(filename="./temp.mp3"))

        volume_num = volume_num - 18
        self.volume(volume_num)

    def block_until_done_playing(self, audio_length):
        while True:
            if self.nest_device.cc.media_controller.status.player_is_idle:
                time.sleep(audio_length)
                break
            time.sleep(0.1)