from dataclasses import dataclass
from typing import Optional

@dataclass
class File:
    id: int
    feature: str
    task: str
    file_name: str
    path: str
    class_name: Optional[str] = None 
