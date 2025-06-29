from pathlib import Path
from typing import Any, Dict, List, Optional
import toml
from automation_db.models.task import Task


class TaskCRUD:
    def __init__(self, path: Path) -> None:
        self.path: Path = path / 'task.toml'

    def _load(self) -> Dict[str, List[Dict[str, Any]]]:
        if self.path.exists():
            return toml.load(self.path.open('r', encoding='utf-8'))
        return {"task": []}

    def _save(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        with self.path.open('w', encoding='utf-8') as f:
            toml.dump(data, f)

    def create(self, task: Task) -> None:
        data = self._load()
        data.setdefault("task", [])
        data["task"].append({
            "name": task.name,
            "requirements": task.requirements,
            "files": task.files,
            "status": task.status
            "feature": task.feature,
            "agent": task.agent,
        })
        self._save(data)

    def read_all(self) -> List[Task]:
        data = self._load()
        return [
            Task(
                name=item["name"],
                requirements=item["requirements"],
                files=item["files"],
                status=item["status"],
                feature=item["feature"],
                agent=item["agent"],
            )
            for item in data.get("task", [])
        ]

    def read_by_feature_and_name(self, feature: str, name: str) -> Task:
        data = self._load()
        for item in data["task"]:
            if item["feature"] == feature and item["name"] == name:
                return Task(
                    name=item["name"],
                    requirements=item["requirements"],
                    files=item["files"],
                    status=item["status"],
                    feature=item["feature"],
                    agent=item["agent"],
                )
        raise ValueError(f"Task with feature '{feature}' and name '{name}' not found")

    def read_by_status(self, status: str = "pending") -> Optional[Task]:
        data = self._load()
        for item in data["task"]:
            if item["status"] == status:
                return Task(
                    name=item["name"],
                    requirements=item["requirements"],
                    files=item["files"],
                    status=item["status"],
                    feature=item["feature"],
                    agent=item["agent"],
                )
        return None

    def update(self, feature: str, name: str, updates: Dict[str, Any]) -> Task:
        data = self._load()
        for item in data["task"]:
            if item["feature"] == feature and item["name"] == name:
                for key, value in updates.items():
                    if key in item:
                        item[key] = value
                self._save(data)
                return Task(
                    name=item["name"],
                    requirements=item["requirements"],
                    files=item["files"],
                    status=item["status"],
                    feature=item["feature"],
                    agent=item["agent"],
                )
        raise ValueError(f"Task with feature '{feature}' and name '{name}' not found")

    def remove(self, feature: str, name: str) -> None:
        data = self._load()
        original_len = len(data["task"])
        data["task"] = [
            item for item in data["task"]
            if not (item["feature"] == feature and item["name"] == name)
        ]
        if len(data["task"]) != original_len:
            self._save(data)

    def add_requirement(self, feature: str, name: str, requirement: str) -> Task:
        task = self.read_by_feature_and_name(feature, name)
        if requirement not in task.requirements:
            task.requirements.append(requirement)
        return self.update(feature, name, {"requirements": task.requirements})

    def update_requirement(self, feature: str, name: str, old: str, new: str) -> Task:
        task = self.read_by_feature_and_name(feature, name)
        if old in task.requirements:
            index = task.requirements.index(old)
            task.requirements[index] = new
        return self.update(feature, name, {"requirements": task.requirements})

    def remove_requirement(self, feature: str, name: str, requirement: str) -> Task:
        task = self.read_by_feature_and_name(feature, name)
        if requirement in task.requirements:
            task.requirements.remove(requirement)
        return self.update(feature, name, {"requirements": task.requirements})
