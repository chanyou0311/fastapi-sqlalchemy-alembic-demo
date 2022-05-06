import uuid

from .config import SessionLocal
from .models import Project, ProjectCreate
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
    def get_project(self, project_id: uuid.UUID) -> Project:
        return self.repo.get_project(project_id)

    @transaction
    def create_project(self, project: Project) -> Project:
        project = self.repo.create_project(project)
        return project

    @transaction
    def create_project_without_pydantic(self, name: str, description: str) -> Project:
        project = Project.create_without_pydantic(name, description)
        project = self.repo.create_project(project)
        return project

    @transaction
    def create_project_with_create_model(self, project: ProjectCreate) -> Project:
        project = Project.create_with_create_model(project)
        project = self.repo.create_project(project)
        return project
