from typing import Any
from pathlib import Path
import toml
from automation_db.models.code_style import CodeStyle


class CodeStyleCRUD:
    def __init__(self, path: Path):
        self.path = path

    def create(self, codestyle: CodeStyle) -> None:
        new_data: dict[str, dict[str, Any]] = {
            'codestyle': {
                'requirements': codestyle.requirements
            }}
        with self.path.open('w') as f:
            toml.dump(new_data, f)

    def read(self) -> CodeStyle:
        data = toml.load(self.path.open())
        return CodeStyle(
            requirements=data['codestyle']['requirements']
        )

    def add_requirement(self, requirement: str) -> CodeStyle:
        current = self.read()
        current.requirements.append(requirement)
        self.create(current)
        return current

    def update_requirement(self, old: str, new: str) -> CodeStyle:
        current = self.read()
        if old in current.requirements:
            index = current.requirements.index(old)
            current.requirements[index] = new
        self.create(current)
        return current

    def remove_requirement(self, requirement: str) -> CodeStyle:
        current = self.read()
        if requirement in current.requirements:
            current.requirements.remove(requirement)
        self.create(current)
        return current
