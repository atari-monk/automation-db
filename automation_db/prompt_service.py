from automation_db.models.context import AutomationContext
from automation_db.prompt_provider import PromptProvider
from automation_db.crud.db_services import DBServices


class PromptService:
    def __init__(self, db: DBServices):
        self.db = db

    def load(self) -> AutomationContext | None:
        task = self.db.task.read_by_status()
        if not task: return None
        agent = self.db.agent.read_by_role(task.agent)
        feature = self.db.feature.read_by_name(task.feature)
        return AutomationContext(project=self.db.project.read(), code_style= self.db.code_style.read(), task=task, agent=agent, feature=feature)

    def update_task(self, context: AutomationContext, status: str = 'implementing'):
        self.db.task.update(context.task.feature, context.task.name, {"status": status})

    def run(self):
        context = self.load()
        if not context:
            print('\nNo pending task\n')
            return
        
        while context:
            print(PromptProvider.generate_prompt(context))
            self.update_task(context)

            context = self.load()
            if not context:
                print('\nNo pending task\n')
                return