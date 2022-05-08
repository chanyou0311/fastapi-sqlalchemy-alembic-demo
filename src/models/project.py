import uuid
from typing import ForwardRef

from pydantic import UUID4
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseDomainModel, BaseOrmModel, BaseDtoModel
from .task import Task


class ProjectOrm(BaseOrmModel):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String(30))
    description = Column(String)
    tasks = relationship("TaskOrm", back_populates="project")


class Project(BaseDomainModel):
    id: UUID4
    name: str
    description: str = ""
    tasks: list[Task] = []

    class Config:
        orm_mode = True
        orm_model = ProjectOrm

    @classmethod
    def create(cls, project: "CreateProjectDto") -> "Project":
        params = project.dict()
        params |= {"id": uuid.uuid4()}
        return cls.parse_obj(params)


class CreateProjectDto(BaseDtoModel):
    name: str
    description: str = ""


Project.update_forward_refs()
