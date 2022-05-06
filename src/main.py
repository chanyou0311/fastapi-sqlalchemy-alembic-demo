import uuid

from fastapi import Body, Depends, FastAPI

from .applications import ProjectApplication
from .config import SessionLocal
from .models import Project, ProjectCreate
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


@app.get("/projects/{id}", response_model=Project)
async def get_project(
    id: uuid.UUID, app: ProjectApplication = Depends(get_project_app)
):
    return app.get_project(id)


@app.post("/projects", response_model=Project)
async def create_project(
    project: Project, app: ProjectApplication = Depends(get_project_app)
):
    return app.create_project(project)


@app.post("/projects/without-pydantic", response_model=Project)
async def create_project_without_pydantic(
    name: str = Body(...),
    description: str = Body(""),
    app: ProjectApplication = Depends(get_project_app),
):
    return app.create_project_without_pydantic(name, description)


@app.post("/projects/with-create-model", response_model=Project)
async def create_project_with_create_model(
    project: ProjectCreate, app: ProjectApplication = Depends(get_project_app)
):
    return app.create_project_with_create_model(project)
