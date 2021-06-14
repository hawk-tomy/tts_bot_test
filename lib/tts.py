from asyncio import AbstractEventLoop, Lock
from audioop import tostereo
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from struct import pack


from discord import PCMAudio


from .jtalk import JTalk


class TTS:
    def __init__(
            self,
            loop: AbstractEventLoop,
            guild_setting: dict,
            dictionary: dict,
    ):
        self.loop = loop
        self.guild_setting = guild_setting
        self.dictionary = dictionary
        self.lock = Lock()
        self.jtalk = JTalk()
        self.exec = ThreadPoolExecutor()

    def update_guild_setting(self, **kwargs):
        self.guild_setting.update(kwargs)

    def add_dictionary(self, key: str, value: str):
        self.dictionary[key] = value

    def update_dictionary(self, **kwargs):
        self.dictionary.update(kwargs)

    def del_dictionary(self, key):
        if key in self.dictionary:
            del self.dictionary[key]

    def clear_dictionary(self):
        self.dictionary.clear()

    def get_source(self, text: str) -> BytesIO:
        pcm = self.jtalk.generate_pcm(text)
        bin_pcm = pack("h"*len(pcm), *pcm)
        return BytesIO(tostereo(bin_pcm, 2, 1, 1))

    def set_voice_setting(
            self,
            voice: str= 'normal',
            speed: float= 1.0,
            tone: float= 0
    ):
        #voice: 'normal', 'happy', 'bashful', 'angry', 'sad'
        #speed: 0.5 - 2
        #tone : -20 - 20
        self.jtalk.set_voice(f'mei_{voice}')
        self.jtalk.set_speed(speed)
        self.jtalk.set_tone(tone)

    async def generate_source(
            self,
            text,
            voice: str= 'normal',
            speed: float= 1.0,
            tone: float= 0
    ):
        async with self.lock:
            self.set_voice_setting(voice, speed, tone)
            pcm = await self.loop.run_in_executor(self.exec, self.get_source, text)
            return PCMAudio(pcm)
