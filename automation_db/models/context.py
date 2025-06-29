from dataclasses import dataclass
from automation_db.models.project import Project
from automation_db.models.code_style import CodeStyle
from automation_db.models.agent import Agent
from automation_db.models.feature import Feature
from automation_db.models.task import Task


@dataclass
class AutomationContext:
    project: Project
    code_style: CodeStyle
    agent: Agent
    feature: Feature
    task: Task