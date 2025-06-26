from pathlib import Path
from typing import List
from automation_db.models.project import Project
from automation_db.models.code_style import CodeStyle
from automation_db.models.feature import Feature
from automation_db.models.agent import Agent
from automation_db.models.file import File
from automation_db.models.task import Task
from automation_db.crud.project_crud import ProjectCRUD
from automation_db.crud.code_style_crud import CodeStyleCRUD
from automation_db.crud.feature_crud import FeatureCRUD
from automation_db.crud.agent_crud import AgentCRUD
from automation_db.crud.file_crud import FileCRUD
from automation_db.crud.task_crud import TaskCRUD
from automation_db.prompt_generator import PromptGenerator


class AutomationContext:
    project: Project
    code_style: CodeStyle
    agent: Agent
    feature: Feature
    file: File
    files: List[File] = []
    task: Task
    prompt: str = ""
    path: Path = Path()
    is_load = False

    def __init__(self):
        from automation_db.config import get_config
        self.config = get_config()
        self.taskCRUD = TaskCRUD(self.config.task)
        self.projectCRUD = ProjectCRUD(self.config.project)
        self.code_styleCRUD = CodeStyleCRUD(self.config.code_style)
        self.agentCRUD = AgentCRUD(self.config.agent)
        self.featureCRUD = FeatureCRUD(self.config.feature) 
        self.fileCRUD = FileCRUD(self.config.file)    

    def _load_task(self) -> bool:
        task = self.taskCRUD.read_by_status()
        if not task:
            return False
        else:
            self.task = task
            return True

    def load(self) -> bool:
        self.project = self.projectCRUD.read()
        self.code_style = self.code_styleCRUD.read()
        if not self._load_task(): return False
        self.agent = self.agentCRUD.read_by_role(self.task.assigned_to)
        self.feature = self.featureCRUD.read_by_name(self.task.feature)
        self.file = self.fileCRUD.read_by_id(self.task.save_file)
        self.files = self.fileCRUD.read_many_by_ids(self.task.context_files)
        self.path = self.project.path / self.file.path / self.file.file_name
        self.is_load = True
        return True

    def generate_prompt(self):
        if not self.is_load:
            print('First load model')
            return
        prompt: List[str] = []
        prompt.append(PromptGenerator.get_project_prompt(self.project))
        prompt.append(PromptGenerator.get_code_style_prompt(self.code_style))
        prompt.append(PromptGenerator.get_feature_prompt(self.feature))
        prompt.append(PromptGenerator.get_agent_prompt(self.agent))
        prompt.append(PromptGenerator.get_file_prompt(self.file))
        prompt.append(PromptGenerator.get_task_prompt(self.task))
        prompt.append(PromptGenerator.get_file_context_prompt(self.project, self.files))
        self.prompt = '\n' + "\n\n".join(prompt)

    def update_task(self, status: str = 'implementing'):
        self.taskCRUD.update(self.task.feature, self.task.name, {"status": status})

    def test(self):
        is_pending = self.load()
        if not is_pending:
            print('\nNo pending task\n')
            return
        
        while is_pending:
            self.generate_prompt()
            print(self.prompt)
            self.update_task()

            is_pending = self.load()
            if not is_pending:
                print('\nNo pending task\n')
                return

def main():
    automation_context = AutomationContext()
    automation_context.test()

if __name__ == '__main__':
    main()