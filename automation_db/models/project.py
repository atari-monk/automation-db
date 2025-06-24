from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class Project:
    name: str
    path: Path
    dependencies: List[str]
    requirements: List[str]