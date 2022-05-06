import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import Select

from . import models


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_project(self, project_id: uuid.UUID) -> models.ProjectSchema:
        statement: Select = select(models.Project).filter_by(id=project_id)
        project_orm = self.session.execute(statement).scalar_one()
        return models.ProjectSchema.from_orm(project_orm)

    def create_project(self, project: models.ProjectSchema) -> models.ProjectSchema:
        self.session.add(project.to_orm())
        return project
