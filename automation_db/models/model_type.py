from enum import Enum


class ModelType(Enum):
    PROJECT = "project"
    CODE_STYLE = "code_style"
    AGENT = "agent"
    FEATURE = "feature"
    FILE = "file"
    TASK = "task"