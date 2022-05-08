import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql import Select

from .models.project import Project, ProjectOrm


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_project(self, project_id: uuid.UUID) -> Project:
        statement: Select = select(ProjectOrm).filter_by(id=str(project_id))
        project_orm = self.session.execute(statement).scalar_one()
        return Project.from_orm(project_orm)

    def create_project(self, project: Project) -> Project:
        self.session.add(project.to_orm())
        return project
