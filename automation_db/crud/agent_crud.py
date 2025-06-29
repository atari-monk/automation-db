from typing import Any
from pathlib import Path
import toml
from automation_db.models.agent import Agent


class AgentCRUD:
    def __init__(self, path: Path):
        self.path = path / 'agent.toml'

    def create(self, agent: Agent) -> None:
        data: dict[str, list[dict[str, object]]] = {'agent': []}
        if self.path.exists():
            data = toml.load(self.path.open())
            if 'agent' not in data:
                data['agent'] = []

        data['agent'].append({
            'role': agent.role,
            'requirements': agent.requirements
        })

        with self.path.open('w') as f:
            toml.dump(data, f)

    def read_all(self) -> list[Agent]:
        data = toml.load(self.path.open())
        return [
            Agent(
                role=agent_data['role'],
                requirements=agent_data['requirements']
            )
            for agent_data in data.get('agent', [])
        ]

    def read_by_role(self, role: str) -> Agent:
        data = toml.load(self.path.open())
        for agent_data in data.get('agent', []):
            if agent_data['role'] == role:
                return Agent(
                    role=agent_data['role'],
                    requirements=agent_data['requirements']
                )
        raise ValueError(f"Agent with role '{role}' not found")

    def update(self, role: str, updates: dict[str, Any]) -> Agent:
        data = toml.load(self.path.open())
        for agent_data in data.get('agent', []):
            if agent_data['role'] == role:
                if 'role' in updates:
                    agent_data['role'] = updates['role']
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Agent(
                    role=agent_data['role'],
                    requirements=agent_data['requirements']
                )
        raise ValueError(f"Agent with role '{role}' not found")

    def add_requirement(self, role: str, requirement: str) -> Agent:
        data = toml.load(self.path.open())
        for agent_data in data.get('agent', []):
            if agent_data['role'] == role:
                agent_data['requirements'].append(requirement)
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Agent(
                    role=agent_data['role'],
                    requirements=agent_data['requirements']
                )
        raise ValueError(f"Agent with role '{role}' not found")

    def update_requirement(self, role: str, old: str, new: str) -> Agent:
        data = toml.load(self.path.open())
        for agent_data in data.get('agent', []):
            if agent_data['role'] == role:
                if old in agent_data['requirements']:
                    index = agent_data['requirements'].index(old)
                    agent_data['requirements'][index] = new
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Agent(
                    role=agent_data['role'],
                    requirements=agent_data['requirements']
                )
        raise ValueError(f"Agent with role '{role}' not found")

    def remove_requirement(self, role: str, requirement: str) -> Agent:
        data = toml.load(self.path.open())
        for agent_data in data.get('agent', []):
            if agent_data['role'] == role:
                if requirement in agent_data['requirements']:
                    agent_data['requirements'].remove(requirement)
                with self.path.open('w') as f:
                    toml.dump(data, f)
                return Agent(
                    role=agent_data['role'],
                    requirements=agent_data['requirements']
                )
        raise ValueError(f"Agent with role '{role}' not found")

    def remove(self, role: str) -> bool:
        data = toml.load(self.path.open())
        agents = data.get('agent', [])
        original_length = len(agents)
        
        data['agent'] = [agent for agent in agents if agent['role'] != role]
        
        removed = original_length != len(data['agent'])
        
        if removed:
            with self.path.open('w') as f:
                toml.dump(data, f)
        
        return removed
