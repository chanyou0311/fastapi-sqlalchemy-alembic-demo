from .applications.project import ProjectApplication
from .applications.task import TaskApplication


def get_project_app():
    return ProjectApplication()


def get_task_app():
    return TaskApplication()
