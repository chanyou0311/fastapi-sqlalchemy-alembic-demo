import uuid
from sqlalchemy.orm import Session

from . import models


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_project(self, project_id: uuid.UUID) -> models.ProjectSchema:
        project = self.session.query(models.Project).get(str(project_id))
        return models.ProjectSchema.from_orm(project)

    def create_project(self, project: models.ProjectSchema) -> models.ProjectSchema:
        self.session.add(project.to_orm())
        return project
