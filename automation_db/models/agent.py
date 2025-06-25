from dataclasses import dataclass
from typing import List

@dataclass
class Agent:
    role: str
    requirements: List[str]
