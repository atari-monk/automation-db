from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Task:
    name: str
    requirements: List[str]
    files: List[Path]
    status: str

    feature: str
    agent: str