from pathlib import Path
from typing import List
from automation_db.project.model import Project
from automation_db.code_style.model import CodeStyle
from automation_db.feature.model import Feature
from automation_db.agent.model import Agent
from automation_db.file.model import File
from automation_db.task.model import Task
from automation_db.project.crud import ProjectCRUD
from automation_db.code_style.crud import CodeStyleCRUD
from automation_db.feature.crud import FeatureCRUD
from automation_db.agent.crud import AgentCRUD
from automation_db.file.crud import FileCRUD
from automation_db.task.crud import TaskCRUD
from automation_db.automation.prompt_generator import PromptGenerator

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

    @classmethod
    def _load_task(cls) -> bool:
        task = TaskCRUD.read_by_status()
        if not task:
            return False
        else:
            cls.task = task
            return True

    @classmethod
    def load(cls) -> bool:
        cls.project = ProjectCRUD.read()
        cls.code_style = CodeStyleCRUD.read()
        if not cls._load_task(): return False
        cls.agent = AgentCRUD.read_by_role(cls.task.assigned_to)
        cls.feature = FeatureCRUD.read_by_name(cls.task.feature)
        cls.file = FileCRUD.read_by_id(cls.task.save_file)
        cls.files = FileCRUD.read_many_by_ids(cls.task.context_files)
        cls.path = cls.project.path / cls.file.path / cls.file.file_name
        cls.is_load = True
        return True

    @classmethod
    def generate_prompt(cls):
        if not cls.is_load:
            print('First load model')
            return
        prompt: List[str] = []
        prompt.append(PromptGenerator.get_project_prompt(cls.project))
        prompt.append(PromptGenerator.get_code_style_prompt(cls.code_style))
        prompt.append(PromptGenerator.get_feature_prompt(cls.feature))
        prompt.append(PromptGenerator.get_agent_prompt(cls.agent))
        prompt.append(PromptGenerator.get_file_prompt(cls.file))
        prompt.append(PromptGenerator.get_task_prompt(cls.task))
        prompt.append(PromptGenerator.get_file_context_prompt(cls.project, cls.files))
        cls.prompt = '\n' + "\n\n".join(prompt)

    @classmethod
    def update_task(cls, status: str = 'implementing'):
        TaskCRUD.update(cls.task.feature, cls.task.name, {"status": status})

    @classmethod
    def test(cls):
        is_pending = cls.load()
        if not is_pending:
            print('\nNo pending task\n')
            return
        
        while is_pending:
            cls.generate_prompt()
            print(cls.prompt)
            cls.update_task()

            is_pending = cls.load()
            if not is_pending:
                print('\nNo pending task\n')
                return

def main():
    automation_context = AutomationContext()
    automation_context.test()

if __name__ == '__main__':
    main()