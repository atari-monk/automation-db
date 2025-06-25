from typing import Any
from pathlib import Path
import toml
from automation_db.models.feature import Feature


class FeatureCRUD:
    def __init__(self, path: Path):
        self.path = path

    def create(self, feature: Feature) -> None:
        data: dict[str, list[dict[str, object]]] = {'feature': []}
        if self.path.exists():
            data = toml.load(self.path.open())
            if 'feature' not in data:
                data['feature'] = []

        data['feature'].append({
            'name': feature.name,
            'requirements': feature.requirements
        })

        with self.path.open('w') as f:
            toml.dump(data, f)

    def read_all(self) -> list[Feature]:
        data = toml.load(self.path.open())
        return [
            Feature(
                name=feature_data['name'],
                requirements=feature_data['requirements']
            )
            for feature_data in data.get('feature', [])
        ]

    def read_by_name(self, name: str) -> Feature:
        data = toml.load(self.path.open())
        for feature_data in data.get('feature', []):
            if feature_data['name'] == name:
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    def update(self, name: str, updates: dict[str, Any]) -> Feature:
        data = toml.load(self.path.open())
        for feature_data in data.get('feature', []):
            if feature_data['name'] == name:
                if 'name' in updates:
                    feature_data['name'] = updates['name']
                if 'status' in updates:
                    feature_data['status'] = updates['status']
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    def add_requirement(self, name: str, requirement: str) -> Feature:
        data = toml.load(self.path.open())
        for feature_data in data.get('feature', []):
            if feature_data['name'] == name:
                feature_data['requirements'].append(requirement)
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    def update_requirement(self, name: str, old: str, new: str) -> Feature:
        data = toml.load(self.path.open())
        for feature_data in data.get('feature', []):
            if feature_data['name'] == name:
                if old in feature_data['requirements']:
                    index = feature_data['requirements'].index(old)
                    feature_data['requirements'][index] = new
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    def remove_requirement(self, name: str, requirement: str) -> Feature:
        data = toml.load(self.path.open())
        for feature_data in data.get('feature', []):
            if feature_data['name'] == name:
                if requirement in feature_data['requirements']:
                    feature_data['requirements'].remove(requirement)
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    def remove(self, name: str) -> None:
        data = toml.load(self.path.open())
        data['feature'] = [
            feature for feature in data.get('feature', [])
            if feature['name'] != name
        ]
        with self.path.open('w') as f:
            toml.dump(data, f)
