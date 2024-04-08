from pydantic import BaseModel
from typing import List
from .sound_option import SoundOption


class SoundSet(BaseModel):
    sound: List[SoundOption]
