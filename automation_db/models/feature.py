from dataclasses import dataclass
from typing import List

@dataclass
class Feature:
    name: str
    requirements: List[str]
