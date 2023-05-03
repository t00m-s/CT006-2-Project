from sqlalchemy.orm import sessionmaker
from .engine import *

Session = sessionmaker(bind=get_engine())
session = Session()


def get_session():
    return session
