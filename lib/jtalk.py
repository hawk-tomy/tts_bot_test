from ctypes import (
    byref,
    c_bool,
    c_char_p,
    c_double,
    c_short,
    c_size_t,
    c_void_p,
    cast,
    cdll,
    POINTER,
    Structure,
    )
from platform import system
from typing import Any, Optional


class HtsVoiceFilelist(Structure):
    _fields_ = [
        ('succ', c_void_p),
        ('path', c_char_p),
        ('name', c_char_p)
        ]


class JTalk:

    MAX_PATH = 260

    def __init__(
            self,
            voice_path_: Optional[str]= None,
            voice_dir_path_: Optional[str]= None,
            dic_path_: Optional[str]= None
    ):
        voice_path = voice_path_ and voice_path_.encode('utf-8')
        voice_dir_path = voice_dir_path_ and voice_dir_path_.encode('utf-8')
        dic_path = dic_path_ and dic_path_.encode('utf-8')

        self._voices: list = []

        if system() == 'Windows':
            lib = 'C:/open_jtalk/bin/jtalk.dll'
        elif system() == 'Darwin':
            lib = 'libjtalk.dylib'
        else:
            lib = 'libjtalk.so'
        self.jtalk = cdll.LoadLibrary(lib)

        self.jtalk.openjtalk_getHTSVoiceList.argtypes = [c_void_p]
        self.jtalk.openjtalk_getHTSVoiceList.restype = POINTER(HtsVoiceFilelist)
        self.jtalk.openjtalk_initialize.argtypes = [c_char_p,c_char_p,c_char_p]
        self.jtalk.openjtalk_initialize.restype = c_void_p
        self.jtalk.openjtalk_setVoice.argtypes = [c_void_p, c_char_p]
        self.jtalk.openjtalk_setSpeed.argtypes = [c_void_p, c_double]
        self.jtalk.openjtalk_setAdditionalHalfTone.argtypes = [c_void_p, c_double]
        self.jtalk.openjtalk_setGvWeightForLogF0.argtypes = [c_void_p, c_double]
        self.jtalk.openjtalk_setVolume.argtypes = [c_void_p, c_double]
        self.jtalk.openjtalk_generatePCM.argtypes = [c_void_p, c_char_p, c_void_p, c_void_p]
        self.jtalk.openjtalk_generatePCM.restype = c_bool

        self.h = self.jtalk.openjtalk_initialize(
            voice_path,
            voice_dir_path,
            dic_path
            )

    def _checkOpenjtalkObject(self):
        if self.h is None:
            raise Exception("Internal Error: OpenJTalk pointer is NULL")

    def _generateVoicelist(self):
        if len(self._voices):
            self._voices.clear()
        link = self.jtalk.openjtalk_getHTSVoiceList(self.h)
        voicelist = link[0]
        while voicelist is not None:
            self._voices.append(
                {
                    'path': voicelist.path.decode('utf-8'),
                    'name': voicelist.name.decode('utf-8')
                }
            )
            if voicelist.succ is None:
                break

    def generate_pcm(self, text: str) -> Any:
        data = c_void_p()
        length = c_size_t()
        r = self.jtalk.openjtalk_generatePCM(
            self.h,
            text.encode('utf-8'),
            byref(data),
            byref(length)
            )
        if not r:
            self.jtalk.openjtalk_clearData(data, length)
            return None

        pcm = cast(data, POINTER(c_short))[:length.value]
        self.jtalk.openjtalk_clearData(data, length)
        return pcm

    def set_voice(self, value: str):
        self._checkOpenjtalkObject()
        self.jtalk.openjtalk_setVoice(self.h, value.encode('utf-8'))

    def set_speed(self, value: float):
        self._check_openjtalk_object()
        self.jtalk.openjtalk_setSpeed(self.h, value)

    def set_tone(self, value: float):
        self._check_openjtalk_object()
        self.jtalk.openjtalk_setAdditionalHalfTone(self.h, value)
