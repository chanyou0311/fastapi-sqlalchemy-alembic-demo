from abc import ABC
import json
from typing import ForwardRef
import uuid
from pydantic import UUID4, BaseModel, Field
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey


mapper_registry = registry()
Base = mapper_registry.generate_base()


class CustomBaseModel(BaseModel, ABC):
    class Config:
        orm_mode = True
        orm_model: Base

    def to_orm(self):
        data = dict(self)
        for key, value in data.items():
            if type(value) == uuid.UUID:
                data[key] = str(value)
            elif isinstance(value, CustomBaseModel):
                data[key] = value.to_orm()
            elif isinstance(value, list):
                data[key] = [
                    v.to_orm() for v in value if isinstance(v, CustomBaseModel)
                ]

        config = self.Config()
        return config.orm_model(**data)


class ProjectORM(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String(30))
    description = Column(String)
    tasks = relationship("TaskORM", back_populates="project")


class TaskORM(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    name = Column(String(30))
    is_completed = Column(Boolean, default=False)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("ProjectORM", back_populates="tasks")


class Project(CustomBaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    description: str = ""
    tasks: list[ForwardRef("Task")] = []

    class Config:
        orm_mode = True
        orm_model = ProjectORM


class Task(CustomBaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    is_completed: bool = False
    project_id: UUID4

    class Config:
        orm_mode = True
        orm_model = TaskORM


Project.update_forward_refs()
