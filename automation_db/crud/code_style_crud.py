from typing import Any
import toml
from automation_db.config import db_config
from automation_db.models import CodeStyle

class CodeStyleCRUD:
    @staticmethod
    def create(codestyle: CodeStyle) -> None:
        new_data: dict[str, dict[str, Any]] = {
            'codestyle': {
                'requirements': codestyle.requirements
            }}
        with db_config.code_style.open('w') as f:
            toml.dump(new_data, f)

    @staticmethod
    def read() -> CodeStyle:
        data = toml.load(db_config.code_style.open())
        return CodeStyle(
            requirements=data['codestyle']['requirements']
        )

    @staticmethod
    def add_requirement(requirement: str) -> CodeStyle:
        current = CodeStyleCRUD.read()
        current.requirements.append(requirement)
        CodeStyleCRUD.create(current)
        return current

    @staticmethod
    def update_requirement(old: str, new: str) -> CodeStyle:
        current = CodeStyleCRUD.read()
        if old in current.requirements:
            index = current.requirements.index(old)
            current.requirements[index] = new
        CodeStyleCRUD.create(current)
        return current

    @staticmethod
    def remove_requirement(requirement: str) -> CodeStyle:
        current = CodeStyleCRUD.read()
        if requirement in current.requirements:
            current.requirements.remove(requirement)
        CodeStyleCRUD.create(current)
        return current