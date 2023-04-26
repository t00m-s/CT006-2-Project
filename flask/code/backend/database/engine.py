from sqlalchemy import *
import os

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

from maps.user import User
from maps.role import Role

def get_engine():
    user = os.getenv('POSTGRES_USER')
    password = (os.getenv('POSTGRES_PASSWORD'))
    db = (os.getenv('POSTGRES_DB'))
    return create_engine(f'postgresql://{user}:{password}@db/{db}')
