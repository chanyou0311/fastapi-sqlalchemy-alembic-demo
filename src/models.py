from typing import ForwardRef
from pydantic import BaseModel
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey


mapper_registry = registry()
Base = mapper_registry.generate_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    description = Column(String)
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    is_completed = Column(Boolean, default=False)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")


class ProjectBaseSchema(BaseModel):
    name: str
    description: str = ""


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectSchema(ProjectBaseSchema):
    id: int
    tasks: list[ForwardRef("TaskSchema")]

    class Config:
        orm_mode = True


class TaskBaseSchema(BaseModel):
    name: str
    is_completed: bool = False


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskSchema(TaskBaseSchema):
    id: int
    project_id: int

    class Config:
        orm_mode = True


ProjectSchema.update_forward_refs()
