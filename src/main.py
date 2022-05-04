from typing import Type
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .applications import ProjectApplication
from .config import settings
from .models import ProjectCreateSchema, ProjectSchema
from .repositories import ProjectRepository

app = FastAPI()
engine = create_engine(settings.database_url)
SessionLocal: Type[Session] = sessionmaker(engine)


def get_project_repo():
    session = SessionLocal()
    return ProjectRepository(session)


def get_project_app(repo: ProjectRepository = Depends(get_project_repo)):
    return ProjectApplication(repo)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/projects/{id}", response_model=ProjectSchema)
async def get_project(id: int, app: ProjectApplication = Depends(get_project_app)):
    return app.get_project(id)


@app.post("/projects", response_model=ProjectSchema)
async def create_project(
    project: ProjectCreateSchema, app: ProjectApplication = Depends(get_project_app)
):
    return app.create_project(project)
