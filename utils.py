from typing import Union
from dataclasses import dataclass


@dataclass
class Subject:
    subject_id: str
    subject_name: str
    subject_credit: int
    prerequisite_credit: Union[int, None] # mostly None, only thesis and prethesis will have this as not None
    is_available: bool
    
@dataclass
class ServerConfig:
    host: str="localhost"
    user: str="root"
    password: str="johnuwu2000"
    database: str="all_course"
