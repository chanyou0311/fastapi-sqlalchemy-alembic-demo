import uuid

from .config import SessionLocal
from .models import ProjectSchema
from .repositories import ProjectRepository


def transaction(func):
    def wrapper(self, *args, **kwargs):
        with self.session.begin():
            return func(self, *args, **kwargs)

    return wrapper


class ProjectApplication:
    def __init__(self) -> None:
        self.session = SessionLocal()
        self.repo = ProjectRepository(self.session)

    @transaction
    def get_project(self, project_id: uuid.UUID) -> ProjectSchema:
        return self.repo.get_project(project_id)

    @transaction
    def create_project(self, project: ProjectSchema) -> ProjectSchema:
        project = self.repo.create_project(project)
        return project
