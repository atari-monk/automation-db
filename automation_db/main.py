from pathlib import Path
from automation_db.crud.project_crud import ProjectCRUD
from automation_db.crud.code_style_crud import CodeStyleCRUD
from automation_db.crud.agent_crud import AgentCRUD
from automation_db.crud.feature_crud import FeatureCRUD
from automation_db.crud.task_crud import TaskCRUD
from automation_db.crud.db_services import DBServices
from automation_db.prompt_service import PromptService


def main():
    path = Path('test')
    db = DBServices(ProjectCRUD(path), CodeStyleCRUD(path),  AgentCRUD(path), FeatureCRUD(path), TaskCRUD(path))
    prompt_service = PromptService(db)
    prompt_service.run()

if __name__ == '__main__':
    main()