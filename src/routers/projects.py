import uuid

from fastapi import APIRouter, Depends, status

from ..applications.project import ProjectApplication
from ..dependencies import get_project_app
from ..models.project import CreateProjectDto, Project

router = APIRouter()


@router.get("/projects", response_model=list[Project])
async def get_projects(app: ProjectApplication = Depends(get_project_app)):
    return app.get_list()


@router.get("/projects/{id}", response_model=Project)
async def get_project(
    id: uuid.UUID,
    app: ProjectApplication = Depends(get_project_app),
):
    return app.get_one(id)


@router.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    dto: CreateProjectDto,
    app: ProjectApplication = Depends(get_project_app),
):
    return app.create(dto)


@router.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: uuid.UUID,
    app: ProjectApplication = Depends(get_project_app),
):
    app.delete(id)
