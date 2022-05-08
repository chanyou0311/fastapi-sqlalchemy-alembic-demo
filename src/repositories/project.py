import json
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from sqlalchemy.sql import Select, Update

from ..models.project import Project, ProjectOrm


class ProjectRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_list(self) -> list[Project]:
        statement: Select = select(ProjectOrm)
        project_orms = self.session.execute(statement).scalars().all()
        return [Project.from_orm(project_orm) for project_orm in project_orms]

    def get_one(self, project_id: uuid.UUID) -> Project:
        statement: Select = select(ProjectOrm).filter_by(id=str(project_id))
        project_orm = self.session.execute(statement).scalar_one()
        return Project.from_orm(project_orm)

    def create(self, project: Project) -> None:
        self.session.add(project.to_orm())
        return project

    def delete(self, project_id: uuid.UUID) -> None:
        statement: Select = delete(ProjectOrm).filter_by(id=str(project_id))
        self.session.execute(statement)

    def update(self, project: Project) -> None:
        params: dict = json.loads(project.json())
        statement: Update = (
            update(ProjectOrm).filter_by(id=str(project.id)).values(**params)
        )
        self.session.execute(statement)
