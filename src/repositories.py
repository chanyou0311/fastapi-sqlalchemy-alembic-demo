from sqlalchemy.orm import Session

from . import models
from .config import settings


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_project(self, project_id: int) -> models.ProjectSchema:
        project = self.session.query(models.Project).get(project_id)
        return models.ProjectSchema.from_orm(project)

    def create_project(self, project: models.ProjectSchema) -> models.ProjectSchema:
        orm_project = models.Project(
            name=project.name,
            description=project.description,
        )
        self.session.add(orm_project)
        return orm_project  # TODO: return value as ProjectSchema
        project = models.ProjectSchema.from_orm(orm_project)
        return project
