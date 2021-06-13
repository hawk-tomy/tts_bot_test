from asyncio import AbstractEventLoop
from audioop import tostereo
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from struct import pack


from discord import PCMAudio


from .jtalk import JTalk


class TTS:
    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop
        self.jtalk = JTalk()
        self.exec = ThreadPoolExecutor()

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
        self.set_voice_setting(voice, speed, tone)
        pcm = await self.loop.run_in_executor(self.exec, self.get_source, text)
        return PCMAudio(pcm)
