import logging

from sqlalchemy.orm import Session

from ceonstock_db import crud
from ceonstock_db import schemas

logger = logging.getLogger(__name__)

LOCAL_PROJECTS_DIR = (
    "/mnt/FileStorage/Dayne/Web/proj_ceonstock/assets/my_cstock_projects"
)
PROJECTS_TO_GET = ["papers_on_desk", "Waving_Flag"]


def get_local_projects():
    pass


def push_local_projects_to_db(
    session: Session,
    projects_dir=LOCAL_PROJECTS_DIR,
    projects_to_get: list[str] = PROJECTS_TO_GET,
):
    logger.info("Pushing default projects (from local filesystem) to db...")
    # TODO actually get projects
    owner = crud.user.get_by_email(session, "admin@ceonstock.com")
    project_to_create = schemas.ProjectCreate(
        title="Existing Project",
        description="This project has existed since the start",
        proj_inputs=[{"test": "abc"}],
        owner_id=owner.id,
    )
    logger.info(f"Creating project; {project_to_create}")
    project_in_db = crud.project.create(session, project_to_create)
    logger.info(f"Created project in db: {project_in_db}")
    return project_in_db


def push_to_db(session: Session):
    owner = crud.user.get_by_email(session, "admin@ceonstock.com")
    project_to_create = schemas.ProjectCreate(
        title="Existing Project",
        description="This project has existed since the start",
        proj_inputs=[{"test": "abc"}],
        owner_id=owner.id,
    )
    logger.info(f"Creating project; {project_to_create}")
    project_in_db = crud.project.create(session, project_to_create)
    logger.info(f"Created project in db: {project_in_db}")
    return project_in_db
