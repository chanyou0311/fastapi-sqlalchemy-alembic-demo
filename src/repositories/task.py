import json
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from sqlalchemy.sql import Select, Update

from ..models.task import Task, TaskOrm


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_list(self) -> list[Task]:
        statement: Select = select(TaskOrm)
        task_orms = self.session.execute(statement).scalars().all()
        return [Task.from_orm(task_orm) for task_orm in task_orms]

    def get_one(self, task_id: uuid.UUID) -> Task:
        statement: Select = select(TaskOrm).filter_by(id=str(task_id))
        task_orm = self.session.execute(statement).scalar_one()
        return Task.from_orm(task_orm)

    def create(self, task: Task) -> None:
        self.session.add(task.to_orm())

    def delete(self, task_id: uuid.UUID) -> None:
        statement: Select = delete(TaskOrm).filter_by(id=str(task_id))
        self.session.execute(statement)

    def update(self, task: Task) -> None:
        params: dict = json.loads(task.json())
        statement: Update = update(TaskOrm).filter_by(id=str(task.id)).values(**params)
        self.session.execute(statement)
