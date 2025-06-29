from automation_db.models.project import Project
from automation_db.models.agent import Agent
from automation_db.models.code_style import CodeStyle
from automation_db.models.feature import Feature
from automation_db.models.task import Task


class PromptGenerator:    
    @staticmethod
    def get_project_prompt(project: Project) -> str:
        prompt = [
            f"Project: {project.name}",
            "Requirements",
            *[f"- {req}" for req in project.requirements],
            "Dependencies",
            *[f"- {dep}" for dep in project.dependencies]
        ]
        return "\n".join(prompt)

    @staticmethod
    def get_agent_prompt(agent: Agent) -> str:
        prompt = [
            f"Agent: {agent.role}",
            *[f"- {spec}" for spec in agent.requirements]
        ]
        return "\n".join(prompt)

    @staticmethod
    def get_code_style_prompt(code_style: CodeStyle) -> str:
        prompt = [
            "Code Style",
            *[f"- {req}" for req in code_style.requirements],
        ]
        return "\n".join(prompt)

    @staticmethod
    def get_feature_prompt(feature: Feature) -> str:
        prompt = [
            f"Feature: {feature.name}",
            "Requirements",
            *[f"- {req}" for req in feature.requirements],
        ]
        return "\n".join(prompt)

    @staticmethod
    def get_task_prompt(task: Task) -> str:
        prompt = [
            f"Task: {task.name}",
            "Requirements:",
            *[f"- {req}" for req in task.requirements]
        ]
        return "\n".join(prompt)
    