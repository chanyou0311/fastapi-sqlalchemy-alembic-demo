import uuid

from fastapi import APIRouter, Depends, status

from ..applications.task import TaskApplication
from ..dependencies import get_task_app
from ..models.task import CreateTaskDto, Task

router = APIRouter()


@router.get("/tasks", response_model=list[Task])
async def get_tasks(app: TaskApplication = Depends(get_task_app)):
    return app.get_list()


@router.get("/tasks/{id}", response_model=Task)
async def get_task(
    id: uuid.UUID,
    app: TaskApplication = Depends(get_task_app),
):
    return app.get_one(id)


@router.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    dto: CreateTaskDto,
    app: TaskApplication = Depends(get_task_app),
):
    return app.create(dto)


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: uuid.UUID,
    app: TaskApplication = Depends(get_task_app),
):
    app.delete(id)
