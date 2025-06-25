from pathlib import Path
import toml
from typing import Any, Dict, List
from automation_db.models.file import File


class FileCRUD:
    def __init__(self, config_file: Path) -> None:
        self.config_file: Path = config_file

    def _load_items(self) -> Dict[str, List[Dict[str, Any]]]:
        if self.config_file.exists():
            with self.config_file.open('r') as f:
                return toml.load(f)
        return {'file': []}

    def _save_items(self, items: Dict[str, List[Dict[str, Any]]]) -> None:
        with self.config_file.open('w') as f:
            toml.dump(items, f)

    def create(self, file: File) -> None:
        items: Dict[str, List[Dict[str, Any]]] = self._load_items()
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
        self._save_items(items)

    def read_by_id(self, id: int) -> File:
        items = self._load_items()
        id_to_item: Dict[int, Dict[str, Any]] = {item['id']: item for item in items.get('file', [])}
        if id not in id_to_item:
            raise FileNotFoundError(f"No file found with ID {id}")
        item: Dict[str, Any] = id_to_item[id]
        return File(
            id=item['id'],
            feature=item['feature'],
            task=item['task'],
            file_name=item['file_name'],
            class_name=item.get('class_name'),
            path=item['path']
        )

    def read_all(self) -> List[File]:
        items = self._load_items()
        files: List[File] = []
        for item in items.get('file', []):
            files.append(File(
                id=item['id'],
                feature=item['feature'],
                task=item['task'],
                file_name=item['file_name'],
                class_name=item.get('class_name'),
                path=item['path']
            ))
        return files

    def read_many_by_feature(self, feature_name: str) -> List[File]:
        items = self._load_items()
        files: List[File] = []
        for item in items.get('file', []):
            if item['feature'] == feature_name:
                files.append(File(
                    id=item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                ))
        return files

    def read_many_by_ids(self, ids: List[int]) -> List[File]:
        items = self._load_items()
        id_to_item: Dict[int, Dict[str, Any]] = {item['id']: item for item in items.get('file', [])}
        selected_files: List[File] = []
        for id_ in ids:
            if id_ in id_to_item:
                item = id_to_item[id_]
                selected_files.append(File(
                    id=item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                ))
        return selected_files

    def read_by_feature_and_task(self, feature_name: str, task_name: str) -> File:
        items = self._load_items()
        for item in items.get('file', []):
            if item['feature'] == feature_name and item['task'] == task_name:
                return File(
                    id=item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                )
        raise ValueError(f"File with feature '{feature_name}' and task '{task_name}' not found")

    def update(self, feature_name: str, task_name: str, updates: Dict[str, Any]) -> File:
        items = self._load_items()
        for item in items.get('file', []):
            if item['feature'] == feature_name and item['task'] == task_name:
                for key, value in updates.items():
                    if key in item:
                        item[key] = value
                self._save_items(items)
                return File(
                    id=item['id'],
                    feature=item['feature'],
                    task=item['task'],
                    file_name=item['file_name'],
                    class_name=item.get('class_name'),
                    path=item['path']
                )
        raise ValueError(f"File with feature '{feature_name}' and task '{task_name}' not found")

    def remove(self, feature_name: str, task_name: str) -> None:
        items = self._load_items()
        items['file'] = [
            item for item in items.get('file', [])
            if not (item['feature'] == feature_name and item['task'] == task_name)
        ]
        self._save_items(items)
