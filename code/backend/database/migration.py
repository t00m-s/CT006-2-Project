from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
import os

from .maps.role import Role
from .maps.type import Type
from .maps.state import State
from .maps.user import User
from .maps.project import Project
from .maps.project_history import ProjectHistory
from .maps.project_files import ProjectFiles
from .maps.chat import Chat
from .session import get_session
from .engine import get_engine


def migrate():
    engine = get_engine()
    db_check = inspect(engine)

    if not db_check.has_table(Role.__tablename__):
        Role.metadata.create_all(engine)
        try:
            get_session().add(Role(id=1, name="Admin", is_reviewer=True))
            get_session().add(Role(id=2, name="Reviewer", is_reviewer=True))
            get_session().add(Role(id=3, name="Researcher", is_reviewer=False))
            get_session().commit()
        except:
            get_session().rollback()

    if not db_check.has_table(Type.__tablename__):
        Type.metadata.create_all(engine)
        try:
            get_session().add(Type(id=1, name="Data Management Plan"))
            get_session().add(Type(id=2, name="Ethics"))
            get_session().add(Type(id=3, name="Deliverable"))
            get_session().commit()
        except:
            get_session().rollback()

    if not db_check.has_table(Type.__tablename__):
        State.metadata.create_all(engine)
    if not db_check.has_table(User.__tablename__):
        User.metadata.create_all(engine)
    if not db_check.has_table(Project.__tablename__):
        Project.metadata.create_all(engine)
    if not db_check.has_table(ProjectHistory.__tablename__):
        ProjectHistory.metadata.create_all(engine)
    if not db_check.has_table(ProjectFiles.__tablename__):
        ProjectFiles.metadata.create_all(engine)
    if not db_check.has_table(Chat.__tablename__):
        Chat.metadata.create_all(engine)

    if not os.path.exists("db_files"):
        os.makedirs("db_files")

    # Raw SQL because docs are not good
    get_session().execute(
        text(
            """
        CREATE OR REPLACE FUNCTION is_reviewer()
        RETURNS TRIGGER AS
        $$
        BEGIN
            IF NEW.id_user_reviewer IS NOT NULL THEN
                IF (NEW.id_user_reviewer NOT IN
                (SELECT u.id
                FROM users u JOIN roles r ON u.id_role=r.id
                WHERE r.is_reviewer AND u.id=NEW.id_user_reviewer) AND
                    (NEW.id_user_reviewer != (SELECT id_user FROM projects WHERE id=NEW.id_project))
                ) THEN
                    RETURN NULL;
                END IF;
            END IF;
            RETURN NEW;
        END $$ LANGUAGE plpgsql;
    """
        )
    )

    get_session().execute(
        text(
            """
            CREATE OR REPLACE TRIGGER is_reviewer_trigger
            BEFORE INSERT OR UPDATE ON project_history
            FOR EACH ROW EXECUTE FUNCTION is_reviewer()
            """
        )
    )
    get_session().commit()
