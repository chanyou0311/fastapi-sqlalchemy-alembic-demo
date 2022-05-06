from abc import ABC
import json
from typing import ForwardRef, Optional
import uuid
from pydantic import UUID4, BaseModel, ConfigError, Field
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey


mapper_registry = registry()
Base = mapper_registry.generate_base()


class CustomBaseModel(BaseModel, ABC):
    class Config:
        orm_mode: bool = False
        orm_model: Optional[Base] = None

    def to_orm(self):
        config = self.Config()
        if config.orm_mode is False or config.orm_model is None:
            raise ConfigError(
                "You must have the config attribute orm_mode=True to use to_orm"
            )
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


class ProjectBase(CustomBaseModel):
    name: str
    description: str = ""


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    tasks: list[ForwardRef("Task")] = []

    class Config:
        orm_mode = True
        orm_model = ProjectORM

    @classmethod
    def create_without_pydantic(cls, name: str, description: str) -> "Project":
        return cls(name=name, description=description)

    @classmethod
    def create_with_create_model(cls, project: "ProjectCreate") -> "Project":
        return cls.parse_obj(project)


class Task(CustomBaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    is_completed: bool = False
    project_id: UUID4

    class Config:
        orm_mode = True
        orm_model = TaskORM


Project.update_forward_refs()
