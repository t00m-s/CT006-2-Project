from sqlalchemy.exc import IntegrityError
import os
from .session import *

engine = get_engine()


def migrate():
    '''
    Loads all ORM classes, then creates the tables
    to the database, then creates db_files directory
    to store the data for each project.
    '''
    from .maps.role import Base, Role
    Base.metadata.create_all(engine)
    try:
        session.add(Role(id=1, name='Admin', is_reviewer=True))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(Role(id=2, name='Reviewer', is_reviewer=True))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(Role(id=3, name='Researcher', is_reviewer=False))
        session.commit()
    except IntegrityError:
        session.rollback()

    from .maps.user import Base
    Base.metadata.create_all(engine)

    from .maps.type import Base
    Base.metadata.create_all(engine)

    from .maps.project import Base
    Base.metadata.create_all(engine)

    from .maps.state import Base, State
    Base.metadata.create_all(engine)
    try:
        session.add(State(id=1, name='Approved', is_closed=True))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(State(id=2, name='Submitted', is_closed=False))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(State(id=3, name='Requires Changes', is_closed=False))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(State(id=4, name='Not Approved', is_closed=True))
        session.commit()
    except IntegrityError:
        session.rollback()

    from .maps.project_history import Base
    Base.metadata.create_all(engine)

    from .maps.project_files import Base
    Base.metadata.create_all(engine)

    if not os.path.exists('db_files'):
        os.makedirs('db_files')
