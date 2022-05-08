import uuid

from fastapi import Body, Depends, FastAPI

from .applications import ProjectApplication
from .config import SessionLocal
from .models.project import Project, CreateProjectDto
from .repositories import ProjectRepository

app = FastAPI()


def get_project_app():
    return ProjectApplication()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/projects/{id}", response_model=Project)
async def get_project(
    id: uuid.UUID,
    app: ProjectApplication = Depends(get_project_app),
):
    return app.get_project(id)


@app.post("/projects", response_model=Project)
async def create_project(
    dto: CreateProjectDto,
    app: ProjectApplication = Depends(get_project_app),
):
    return app.create_project(dto)
