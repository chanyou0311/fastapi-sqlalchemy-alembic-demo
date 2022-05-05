from typing import ForwardRef
import uuid
from pydantic import UUID4, BaseModel, Field
from sqlalchemy.orm import registry, relationship
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey


mapper_registry = registry()
Base = mapper_registry.generate_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True)
    name = Column(String(30))
    description = Column(String)
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    name = Column(String(30))
    is_completed = Column(Boolean, default=False)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")


class ProjectSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    description: str = ""
    tasks: list[ForwardRef("TaskSchema")] = []

    class Config:
        orm_mode = True

    def to_orm(self):
        return Project(
            id=str(self.id),
            name=self.name,
            description=self.description,
            tasks=[task.to_orm() for task in self.tasks],
        )


class TaskSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str
    is_completed: bool = False
    project_id: UUID4

    class Config:
        orm_mode = True

    def to_orm(self):
        return Task(
            id=str(self.id),
            name=self.name,
            is_completed=self.is_completed,
            project_id=self.project_id,
        )


ProjectSchema.update_forward_refs()
