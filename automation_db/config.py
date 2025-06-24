from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, ClassVar

from automation_db.cli.model_type import ModelType

@dataclass(frozen=True)
class DbConfig:
    race_game = r"C:\atari-monk\code\race-track-game\automation_db"
    arcade = r"C:\atari-monk\code\explore-arcade\automation_db"
    db_folder: Path = Path(arcade)

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

db_config = DbConfig()

if __name__ == '__main__':
    print(f'db_folder: {db_config.db_folder}')
    
    print(f'project: {db_config.project}')
    print(f'code_style: {db_config.code_style}')
    print(f'agent: {db_config.agent}')
    print(f'feature: {db_config.feature}')
    print(f'file: {db_config.file}')
    print(f'task: {db_config.task}')

    print(f'db_config[ModelType.AGENT]: {db_config[ModelType.AGENT]}')
