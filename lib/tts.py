from .jtalk import JTalk


class TTS:
    def __init__(self):
        self.jtalk = JTalk()

    def set_voice_setting(
            self,
            voice: str,
            speed: float,
            tone: float
    ):
        #voice: 'normal', 'happy', 'bashful', 'angry', 'sad'
        #speed: 0.5 - 2
        #tone : -20 - 20
        self.jtalk.set_voice(f'mei_{voice}')
        self.jtalk.set_speed(speed)
        self.jtalk.set_tone(tone)
