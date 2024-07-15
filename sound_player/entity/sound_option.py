from pydantic import BaseModel
from typing import List


class SoundOption(BaseModel):
    group: str
    code: str
    type: str
    count: str
    topic: str
    priority: int
    task_code: str = None
    status: List[str]
