import uuid

from fastapi import Depends, FastAPI

from .applications import ProjectApplication
from .config import SessionLocal
from .models import ProjectSchema
from .repositories import ProjectRepository

app = FastAPI()


def get_project_repo():
    session = SessionLocal()
    return ProjectRepository(session)


def get_project_app(repo: ProjectRepository = Depends(get_project_repo)):
    return ProjectApplication()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/projects/{id}", response_model=ProjectSchema)
async def get_project(
    id: uuid.UUID, app: ProjectApplication = Depends(get_project_app)
):
    return app.get_project(id)


@app.post("/projects", response_model=ProjectSchema)
async def create_project(
    project: ProjectSchema, app: ProjectApplication = Depends(get_project_app)
):
    return app.create_project(project)
