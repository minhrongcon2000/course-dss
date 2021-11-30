from typing import List, Tuple, Union
import networkx as nx
import matplotlib.pyplot as plt
import mysql.connector as connector
from dataclasses import dataclass


@dataclass
class Subject:
    subject_id: str
    subject_name: str
    subject_credit: int
    prerequisite_credit: Union[int, None] # mostly None, only thesis and prethesis will have this as not None