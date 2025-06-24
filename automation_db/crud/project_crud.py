from pathlib import Path
import toml
from typing import Any
from automation_db.project.model import Project
from automation_db.db.config import db_config

class ProjectCRUD:
    @staticmethod
    def create(project: Project) -> None:
        new_data: dict[str, dict[str, Any]] = {
                'project': {
                    'name': project.name,
                    'path': str(project.path),
                    'dependencies': project.dependencies,
                    'requirements': project.requirements
                }}
        with db_config.project.open('w') as f:
            toml.dump(new_data, f)

    @staticmethod
    def read() -> Project:
        data = toml.load(db_config.project.open())
        return Project(
            name=data['project']['name'],
            path=Path(data['project']['path']),
            dependencies=data['project']['dependencies'],
            requirements=data['project']['requirements']
        )

    @staticmethod
    def update(updates: dict[str, Any]) -> Project:
        current = ProjectCRUD.read()
        if 'name' in updates:
            current.name = updates['name']
        if 'path' in updates:
            current.path = Path(updates['path'])
        ProjectCRUD.create(current)
        return current

    @staticmethod
    def add_dependency(dependency: str) -> Project:
        current = ProjectCRUD.read()
        current.dependencies.append(dependency)
        ProjectCRUD.create(current)
        return current

    @staticmethod
    def add_requirement(requirement: str) -> Project:
        current = ProjectCRUD.read()
        current.requirements.append(requirement)
        ProjectCRUD.create(current)
        return current

    @staticmethod
    def update_dependency(old: str, new: str) -> Project:
        current = ProjectCRUD.read()
        if old in current.dependencies:
            index = current.dependencies.index(old)
            current.dependencies[index] = new
        ProjectCRUD.create(current)
        return current

    @staticmethod
    def update_requirement(old: str, new: str) -> Project:
        current = ProjectCRUD.read()
        if old in current.requirements:
            index = current.requirements.index(old)
            current.requirements[index] = new
        ProjectCRUD.create(current)
        return current

    @staticmethod
    def remove_dependency(dependency: str) -> Project:
        current = ProjectCRUD.read()
        if dependency in current.dependencies:
            current.dependencies.remove(dependency)
        ProjectCRUD.create(current)
        return current

    @staticmethod
    def remove_requirement(requirement: str) -> Project:
        current = ProjectCRUD.read()
        if requirement in current.requirements:
            current.requirements.remove(requirement)
        ProjectCRUD.create(current)
        return current