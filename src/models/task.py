import uuid
from pydantic import UUID4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseDomainModel, BaseOrmModel, BaseDtoModel


class TaskOrm(BaseOrmModel):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True)
    name = Column(String(30))
    is_completed = Column(Boolean, default=False)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("ProjectOrm", back_populates="tasks")


class Task(BaseDomainModel):
    id: UUID4
    name: str
    is_completed: bool = False
    project_id: UUID4

    class Config:
        orm_mode = True
        orm_model = TaskOrm

    @classmethod
    def create(cls, task: "CreateTaskDto") -> "Task":
        params = task.dict()
        params |= {"id": uuid.uuid4()}
        return cls.parse_obj(params)


class CreateTaskDto(BaseDtoModel):
    name: str
    project_id: UUID4
