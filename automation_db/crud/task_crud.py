import toml
from automation_db.task.model import Task
from typing import Any

from automation_db.db.config import db_config

class TaskCRUD:
    @staticmethod
    def create(task: Task) -> None:
        items: dict[str, list[dict[str, object]]] = {'task': []}
        if db_config.task.exists():
            items = toml.load(db_config.task.open())
            if 'task' not in items:
                items['task'] = []
        
        items['task'].append({
            'feature': task.feature,
            'name': task.name,
            'requirements': task.requirements,
            'context_files': task.context_files,
            'save_file': task.save_file,
            'assigned_to': task.assigned_to,
            'status': task.status
        })
        
        with db_config.task.open('w') as f:
            toml.dump(items, f)

    @staticmethod
    def read_all() -> list[Task]:
        items = toml.load(db_config.task.open())
        return [
            Task(
                feature=item['feature'],
                name=item['name'],
                requirements=item['requirements'],
                assigned_to=item['assigned_to'],
                context_files=item['context_files'],
                save_file=item['save_file'],
                status=item['status'])
            for item in items['task']
        ]
    
    @staticmethod
    def read_by_feature_and_name(feature: str, name: str) -> Task:
        items = toml.load(db_config.task.open())
        for item in items['task']:
            if item['feature'] == feature and item['name'] == name:
                return Task(
                    feature=item['feature'],
                    name=item['name'],
                    requirements=item['requirements'],
                    context_files=item['context_files'],
                    save_file=item['save_file'],
                    assigned_to=item['assigned_to'],
                    status=item['status']
                )
        raise ValueError(f"Task with feature '{feature}' and name '{name}' not found")

    @staticmethod
    def read_by_status(status: str = 'pending') -> Task | None:
        items = toml.load(db_config.task.open())
        for item in items['task']:
            if item['status'] == status:
                return Task(
                    feature=item['feature'],
                    name=item['name'],
                    requirements=item['requirements'],
                    context_files=item['context_files'],
                    save_file=item['save_file'],
                    assigned_to=item['assigned_to'],
                    status=item['status']
                )
        return None

    @staticmethod
    def update(feature: str, name: str, updates: dict[str, Any]) -> Task:
        items = toml.load(db_config.task.open())
        for item in items['task']:
            if item['feature'] == feature and item['name'] == name:
                for key, value in updates.items():
                    if key in item:
                        item[key] = value
                with db_config.task.open('w') as f:
                    toml.dump(items, f)
                return Task(
                    feature=item['feature'],
                    name=item['name'],
                    requirements=item['requirements'],
                    context_files=item['context_files'],
                    save_file=item['save_file'],
                    assigned_to=item['assigned_to'],
                    status=item['status']
                )
        raise ValueError(f"Task with feature '{feature}' and name '{name}' not found")

    @staticmethod
    def remove(feature: str, name: str) -> None:
        items = toml.load(db_config.task.open())
        items['task'] = [item for item in items['task'] if not (item['feature'] == feature and item['name'] == name)]
        with db_config.task.open('w') as f:
            toml.dump(items, f)

    @staticmethod
    def add_requirement(feature: str, name: str, requirement: str) -> Task:
        item = TaskCRUD.read_by_feature_and_name(feature, name)
        item.requirements.append(requirement)
        updates = {'requirements': item.requirements}
        return TaskCRUD.update(feature, name, updates)

    @staticmethod
    def update_requirement(feature: str, name: str, old: str, new: str) -> Task:
        item = TaskCRUD.read_by_feature_and_name(feature, name)
        if old in item.requirements:
            index = item.requirements.index(old)
            item.requirements[index] = new
        updates = {'requirements': item.requirements}
        return TaskCRUD.update(feature, name, updates)

    @staticmethod
    def remove_requirement(feature: str, name: str, requirement: str) -> Task:
        item = TaskCRUD.read_by_feature_and_name(feature, name)
        if requirement in item.requirements:
            item.requirements.remove(requirement)
        updates = {'requirements': item.requirements}
        return TaskCRUD.update(feature, name, updates)