from pathlib import Path
from typing import List
from automation_db.models.project import Project
from automation_db.models.agent import Agent
from automation_db.models.code_style import CodeStyle
from automation_db.models.feature import Feature
from automation_db.models.task import Task
from automation_db.models.context import AutomationContext


class PromptProvider:    
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
    
    @staticmethod
    def get_file_context_prompt(files: List[Path]) -> str:
        if not files:
            return ""
        
        file_sections: list[str] = []
        
        for file_path in files:
            file_header = f"File: {file_path}"
            
            if not file_path.exists():
                file_sections.append(f"{file_header} - NOT FOUND")
                continue
                
            try:
                content = file_path.read_text().strip()
                file_sections.append(f"{file_header}\n{content}")
            except Exception as e:
                file_sections.append(f"{file_header} - ERROR READING FILE: {str(e)}")
        
        return "Code Context:\n\n" + "\n\n".join(file_sections) + "\n"
    
    @staticmethod
    def generate_prompt(context: AutomationContext):
        prompt: List[str] = []
        prompt.append(PromptProvider.get_project_prompt(context.project))
        prompt.append(PromptProvider.get_code_style_prompt(context.code_style))
        prompt.append(PromptProvider.get_feature_prompt(context.feature))
        prompt.append(PromptProvider.get_agent_prompt(context.agent))
        prompt.append(PromptProvider.get_task_prompt(context.task))
        prompt.append(PromptProvider.get_file_context_prompt(context.task.files))
        return '\n' + "\n\n".join(prompt)