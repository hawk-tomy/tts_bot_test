from dataclasses import dataclass


from bot_util.config import config, ConfigBase


extension = tuple(
     f'{__name__}.{name}' for name in (
         'tts',
     )
)


@dataclass
class EmbedSetting(ConfigBase):
    color: int= 0x54c3f1

config.add_default_config(EmbedSetting, key='embed_setting')
