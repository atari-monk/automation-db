from typing import List
from automation_db.project.model import Project
from automation_db.agent.model import Agent
from automation_db.code_style.model import CodeStyle
from automation_db.feature.model import Feature
from automation_db.file.model import File
from automation_db.task.model import Task

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
    def get_file_prompt(file: File) -> str:
        file_prompt = [
             "File:",
            f"- file name: {file.file_name}",
            f"- path: {file.path}",
        ]
        if file.class_name:
            file_prompt.append(f"- class name: {file.class_name}")
        return "\n".join(file_prompt)

    @staticmethod
    def get_task_prompt(task: Task) -> str:
        prompt = [
            f"Task: {task.name}",
            "Requirements:",
            *[f"- {req}" for req in task.requirements]
        ]
        return "\n".join(prompt)
    
    @staticmethod
    def get_file_context_prompt(project: Project, files: List[File]) -> str:
        if not files:
            return ""  # Return empty string if no files provided
        
        file_sections: list[str] = []
        
        for file in files:
            full_path = project.path / file.path / file.file_name
            file_header = f"File: {full_path}"
            
            if not full_path.exists():
                file_sections.append(f"{file_header} - NOT FOUND")
                continue
                
            try:
                with open(full_path, 'r') as f:
                    content = f.read().strip()
                    file_sections.append(f"{file_header}\n{content}")
            except Exception as e:
                file_sections.append(f"{file_header} - ERROR READING FILE: {str(e)}")
        
        # Add the header and join all sections
        return "Code Context:\n\n" + "\n\n".join(file_sections) + "\n"