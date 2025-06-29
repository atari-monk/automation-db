from dataclasses import dataclass
from automation_db.crud.project_crud import ProjectCRUD
from automation_db.crud.code_style_crud import CodeStyleCRUD
from automation_db.crud.task_crud import TaskCRUD
from automation_db.crud.agent_crud import AgentCRUD
from automation_db.crud.feature_crud import FeatureCRUD


@dataclass
class DBServices:
    project: ProjectCRUD
    code_style: CodeStyleCRUD
    agent: AgentCRUD
    feature: FeatureCRUD
    task: TaskCRUD