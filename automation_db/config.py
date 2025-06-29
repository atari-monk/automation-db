from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, ClassVar
from automation_db.models.model_type import ModelType


@dataclass(frozen=True)
class DbConfig:
    db_folder: Path

    project: Path = field(init=False)
    code_style: Path = field(init=False)
    agent: Path = field(init=False)
    feature: Path = field(init=False)
    file: Path = field(init=False)
    task: Path = field(init=False)

    _model_filenames: ClassVar[Dict[str, str]] = {
        "project": "project.toml",
        "code_style": "code_style.toml",
        "agent": "agent.toml",
        "feature": "feature.toml",
        "file": "file.toml",
        "task": "task.toml"
    }

    def __post_init__(self):
        for attr_name, file_name in self._model_filenames.items():
            object.__setattr__(self, attr_name, self.db_folder / file_name)

    def __getitem__(self, model_type: ModelType) -> Path:
        attr_name = model_type.value
        return getattr(self, attr_name)


_config_instance: DbConfig | None = None

def get_config(db_folder: Path) -> DbConfig:
    global _config_instance
    if _config_instance is None:
        _config_instance = DbConfig(db_folder)
    return _config_instance
