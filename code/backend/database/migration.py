from sqlalchemy.exc import IntegrityError

from .session import *

engine = get_engine()

'''
Loads all ORM classes and then creates the tables
to the database.
'''


def migrate():
    from .maps.role import Base, Role
    Base.metadata.create_all(engine)
    try:
        session.add(Role(name='Admin', is_reviewer=True))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(Role(name='Reviewer', is_reviewer=True))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(Role(name='Researcher', is_reviewer=False))
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
        session.add(State(name='Approved', is_closed=True))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(State(name='Submitted', is_closed=False))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(State(name='Requires Changes', is_closed=False))
        session.commit()
    except IntegrityError:
        session.rollback()
    try:
        session.add(State(name='Not Approved', is_closed=True))
        session.commit()
    except IntegrityError:
        session.rollback()

    from .maps.project_history import Base
    Base.metadata.create_all(engine)

    from .maps.project_files import Base
    Base.metadata.create_all(engine)
