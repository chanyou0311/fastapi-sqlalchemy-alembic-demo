import uuid

from ..config import SessionLocal
from ..models.task import Task, CreateTaskDto
from ..repositories.task import TaskRepository
from .base import transaction


class TaskApplication:
    def __init__(self) -> None:
        self.session = SessionLocal()
        self.repo = TaskRepository(self.session)

    @transaction
    def get_list(self) -> list[Task]:
        return self.repo.get_list()

    @transaction
    def get_one(self, task_id: uuid.UUID) -> Task:
        return self.repo.get_one(task_id)

    @transaction
    def create(self, dto: CreateTaskDto) -> Task:
        task = Task.create(dto)
        self.repo.create(task)
        return task

    @transaction
    def delete(self, task_id: uuid.UUID) -> Task:
        return self.repo.delete(task_id)

    @transaction
    def complete(self, task_id: uuid.UUID) -> Task:
        task = self.repo.get_one(task_id)
        task.complete()
        self.repo.update(task)
        return task
