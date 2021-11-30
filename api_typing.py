from typing import List, Set
from pydantic import BaseModel


class Progress(BaseModel):
    studied_subjects: List[Set[str]]
