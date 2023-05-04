from .engine import *

engine = get_engine()

'''
Loads all ORM classes and then creates the tables
to the database.
'''
# TODO find a better way to do this
def migrate():
    from .maps.role import Base
    Base.metadata.create_all(engine)

    from .maps.user import Base
    Base.metadata.create_all(engine)

    from .maps.type import Base
    Base.metadata.create_all(engine)

    from .maps.project import Base
    Base.metadata.create_all(engine)

    from .maps.state import Base
    Base.metadata.create_all(engine)

    from .maps.project_history import Base
    Base.metadata.create_all(engine)

    from .maps.project_files import Base
    Base.metadata.create_all(engine)
