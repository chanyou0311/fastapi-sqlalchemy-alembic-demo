import uuid

from fastapi import Body, Depends, FastAPI, Response, status


from .applications import ProjectApplication
from .config import SessionLocal
from .models.project import CreateProjectDto, Project
from .repositories import ProjectRepository

app = FastAPI()


def get_project_app():
    return ProjectApplication()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/projects", response_model=list[Project])
async def get_projects(app: ProjectApplication = Depends(get_project_app)):
    return app.get_list()


@app.get("/projects/{id}", response_model=Project)
async def get_project(
    id: uuid.UUID,
    app: ProjectApplication = Depends(get_project_app),
):
    return app.get_one(id)


@app.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    dto: CreateProjectDto,
    app: ProjectApplication = Depends(get_project_app),
):
    return app.create(dto)


@app.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    id: uuid.UUID,
    app: ProjectApplication = Depends(get_project_app),
):
    app.delete(id)
