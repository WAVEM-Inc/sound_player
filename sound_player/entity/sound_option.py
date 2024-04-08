from pydantic import BaseModel
from typing import List


class SoundOption(BaseModel):
    code: str
    type: str
    count: str
    topic: str
    priority: int
    status: List[str]
