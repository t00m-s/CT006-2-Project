from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
import os

from .session import get_session
from .engine import get_engine

engine = get_engine()


def migrate():
    """
    Loads all ORM classes, then creates the tables
    to the database, then creates db_files directory
    to store the data for each project.
    """
    from .maps.role import Base, Role

    Base.metadata.create_all(engine)
    if not get_session().query(Role).first():
        try:
            get_session().add(Role(id=1, name="Admin", is_reviewer=True))
            get_session().add(Role(id=2, name="Reviewer", is_reviewer=True))
            get_session().add(Role(id=3, name="Researcher", is_reviewer=False))
            get_session().commit()
        except:
            get_session().rollback()

    from .maps.user import Base

    Base.metadata.create_all(engine)

    from .maps.type import Base, Type

    Base.metadata.create_all(engine)

    if not get_session().query(Type).first():
        try:
            get_session().add(Type(id=1, name="Data Management Plan"))
            get_session().add(Type(id=2, name="Ethics"))
            get_session().add(Type(id=3, name="Deliverable"))
            get_session().commit()
        except:
            get_session().rollback()

    from .maps.project import Base

    Base.metadata.create_all(engine)

    from .maps.state import Base, State

    Base.metadata.create_all(engine)
    if not get_session().query(State).first():
        try:
            get_session().add(State(id=1, name="Approved", is_closed=True))
            get_session().add(State(id=2, name="Submitted", is_closed=False))
            get_session().add(State(id=3, name="Requires Changes", is_closed=False))
            get_session().add(State(id=4, name="Not Approved", is_closed=True))
            get_session().commit()
        except:
            get_session().rollback()

    from .maps.project_history import Base

    Base.metadata.create_all(engine)

    from .maps.project_files import Base

    Base.metadata.create_all(engine)

    from .maps.chat import Base

    Base.metadata.create_all(engine)

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
