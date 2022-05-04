from .models import ProjectCreateSchema, ProjectSchema
from .repositories import ProjectRepository


class ProjectApplication:
    def __init__(self, repo: ProjectRepository) -> None:
        self.repo = repo

    def get_project(self, project_id: int) -> ProjectSchema:
        return self.repo.get_project(project_id)

    def create_project(self, project: ProjectCreateSchema) -> ProjectSchema:
        # TODO: implement transaction processing
        with self.repo.session.begin():
            project = self.repo.create_project(project)
        return ProjectSchema.from_orm(project)
        # return project
