from pathlib import Path
from typing import Any
import toml
from automation_db.models.project import Project


class ProjectCRUD:
    def __init__(self, path: Path):
        self.path = path / 'project.toml'

    def create(self, project: Project) -> None:
        new_data: dict[str, dict[str, Any]] = {
            'project': {
                'name': project.name,
                'path': str(project.path),
                'dependencies': project.dependencies,
                'requirements': project.requirements
            }
        }
        with self.path.open('w') as f:
            toml.dump(new_data, f)

    def read(self) -> Project:
        data = toml.load(self.path.open())
        return Project(
            name=data['project']['name'],
            path=Path(data['project']['path']),
            dependencies=data['project']['dependencies'],
            requirements=data['project']['requirements']
        )

    def update(self, updates: dict[str, Any]) -> Project:
        current = self.read()
        if 'name' in updates:
            current.name = updates['name']
        if 'path' in updates:
            current.path = Path(updates['path'])
        self.create(current)
        return current

    def add_dependency(self, dependency: str) -> Project:
        current = self.read()
        current.dependencies.append(dependency)
        self.create(current)
        return current

    def add_requirement(self, requirement: str) -> Project:
        current = self.read()
        current.requirements.append(requirement)
        self.create(current)
        return current

    def update_dependency(self, old: str, new: str) -> Project:
        current = self.read()
        if old in current.dependencies:
            index = current.dependencies.index(old)
            current.dependencies[index] = new
        self.create(current)
        return current

    def update_requirement(self, old: str, new: str) -> Project:
        current = self.read()
        if old in current.requirements:
            index = current.requirements.index(old)
            current.requirements[index] = new
        self.create(current)
        return current

    def remove_dependency(self, dependency: str) -> Project:
        current = self.read()
        if dependency in current.dependencies:
            current.dependencies.remove(dependency)
        self.create(current)
        return current

    def remove_requirement(self, requirement: str) -> Project:
        current = self.read()
        if requirement in current.requirements:
            current.requirements.remove(requirement)
        self.create(current)
        return current
