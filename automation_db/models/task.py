from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    feature: str
    name: str
    requirements: List[str]
    context_files: List[int]
    save_file: int
    assigned_to: str
    status: str

