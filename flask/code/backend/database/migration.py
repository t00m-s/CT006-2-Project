from .engine import *

engine = get_engine()


def migrate():
    from .maps.role import Role, Base
    Base.metadata.create_all(engine)

    from .maps.user import User, Base
    Base.metadata.create_all(engine)

    from .maps.type import Type, Base
    Base.metadata.create_all(engine)