import toml
from typing import Any, List
from automation_db.db.config import db_config
from automation_db.file.model import File

class FileCRUD:
    @staticmethod
    def create(file: File) -> None:
        items: dict[str, list[dict[str, object]]] = {'file': []}
        if db_config.file.exists():
            items = toml.load(db_config.file.open())
            if 'file' not in items:
                items['file'] = []
        
        items['file'].append({
            'id': file.id,
            'feature': file.feature,
            'task': file.task,
            'file_name': file.file_name,
            'class_name': file.class_name,
            'path': file.path
        })
        
        with db_config.file.open('w') as f:
            toml.dump(items, f)

    @staticmethod
    def read_by_id(id: int) -> File:
        items = toml.load(db_config.file.open())
        id_to_item = {item['id']: item for item in items['file']}
        
        if id not in id_to_item:
            raise FileNotFoundError(f"No file found with ID {id}")
        
        item = id_to_item[id]
        return File(
            id=item['id'],
            feature=item['feature'],
            task=item['task'],
            file_name=item['file_name'],
            class_name=item.get('class_name'),
            path=item['path']
        )

    @staticmethod
    def read_all() -> List[File]:
        file_items = toml.load(db_config.file.open())
        items: List[File] = []
        for item in file_items['file']:
            items.append(File(
                id = item['id'],
                feature=item['feature'],
                task=item['task'],
                file_name=item['file_name'],
                class_name=item.get('class_name'),
                path=item['path']
            ))
        return items
    
    @staticmethod
    def read_many_by_feature(feature_name: str) -> List[File]:
        file_items = toml.load(db_config.file.open())
        items: List[File] = []
        for item in file_items['file']:
            if item['feature'] == feature_name:
                items.append(File(
                    id = item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                ))
        return items
    
    @staticmethod
    def read_many_by_ids(ids: List[int]) -> List[File]:
        items = toml.load(db_config.file.open())
        id_to_item = {item['id']: item for item in items['file']}
        
        select_items: List[File] = []
        for id in ids:
            if id in id_to_item:
                item = id_to_item[id]
                select_items.append(File(
                    id=item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                ))
        return select_items
    
    @staticmethod
    def read_by_feature_and_task(feature_name: str, task_name: str) -> File:
        items = toml.load(db_config.file.open())
        for item in items['file']:
            if item['feature'] == feature_name and item['task'] == task_name:
                return File(
                    id = item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                )
        raise ValueError(f"File with feature '{feature_name}' and task '{task_name}' not found")

    @staticmethod
    def update(feature_name: str, task_name: str, updates: dict[str, Any]) -> File:
        items = toml.load(db_config.file.open())
        for item in items['file']:
            if item['feature'] == feature_name and item['task'] == task_name:
                for key, value in updates.items():
                    if key in item:
                        item[key] = value
                with db_config.file.open('w') as f:
                    toml.dump(items, f)
                return File(
                    id = item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                )
        raise ValueError(f"FeatureFile with feature '{feature_name}' and task '{task_name}' not found")

    @staticmethod
    def remove(feature_name: str, task_name: str) -> None:
        items = toml.load(db_config.file.open())
        items['file'] = [
            item for item in items['file']
            if not (item['feature'] == feature_name and item['task'] == task_name)
        ]
        with db_config.file.open('w') as f:
            toml.dump(items, f)