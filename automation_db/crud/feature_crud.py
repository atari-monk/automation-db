from typing import Any
import toml
from automation_db.db.config import db_config
from automation_db.feature.model import Feature

class FeatureCRUD:
    @staticmethod
    def create(feature: Feature) -> None:
        data: dict[str, list[dict[str, object]]] = {'feature': []}
        if db_config.feature.exists():
            data = toml.load(db_config.feature.open())
            if 'feature' not in data:
                data['feature'] = []
        
        data['feature'].append({
            'name': feature.name,
            'requirements': feature.requirements
        })
        
        with db_config.feature.open('w') as f:
            toml.dump(data, f)

    @staticmethod
    def read_all() -> list[Feature]:
        data = toml.load(db_config.feature.open())
        return [
            Feature(
                name=feature_data['name'],
                requirements=feature_data['requirements'])
            for feature_data in data['feature']
        ]
    
    @staticmethod
    def read_by_name(name: str) -> Feature:
        data = toml.load(db_config.feature.open())
        for feature_data in data['feature']:
            if feature_data['name'] == name:
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    @staticmethod
    def update(name: str, updates: dict[str, Any]) -> Feature:
        data = toml.load(db_config.feature.open())
        for feature_data in data['feature']:
            if feature_data['name'] == name:
                if 'name' in updates:
                    feature_data['name'] = updates['name']
                if 'status' in updates:
                    feature_data['status'] = updates['status']
                with db_config.feature.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    @staticmethod
    def add_requirement(name: str, requirement: str) -> Feature:
        data = toml.load(db_config.feature.open())
        for feature_data in data['feature']:
            if feature_data['name'] == name:
                feature_data['requirements'].append(requirement)
                with db_config.feature.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    @staticmethod
    def update_requirement(name: str, old: str, new: str) -> Feature:
        data = toml.load(db_config.feature.open())
        for feature_data in data['feature']:
            if feature_data['name'] == name:
                if old in feature_data['requirements']:
                    index = feature_data['requirements'].index(old)
                    feature_data['requirements'][index] = new
                with db_config.feature.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    @staticmethod
    def remove_requirement(name: str, requirement: str) -> Feature:
        data = toml.load(db_config.feature.open())
        for feature_data in data['feature']:
            if feature_data['name'] == name:
                if requirement in feature_data['requirements']:
                    feature_data['requirements'].remove(requirement)
                with db_config.feature.open('w') as f:
                    toml.dump(data, f)
                return Feature(
                    name=feature_data['name'],
                    requirements=feature_data['requirements']
                )
        raise ValueError(f"Feature with name '{name}' not found")

    @staticmethod
    def remove(name: str) -> None:
        data = toml.load(db_config.feature.open())
        data['feature'] = [feature for feature in data['feature'] if feature['name'] != name]
        with db_config.feature.open('w') as f:
            toml.dump(data, f)