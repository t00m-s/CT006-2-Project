from sqlalchemy import *
from sqlachemy.orm import *
import os


def get_engine():
    user = os.getenv('POSTGRES_USER')
    password = (os.getenv('POSTGRES_PASSWORD'))
    db = (os.getenv('POSTGRES_DB'))
    return create_engine(f'postgresql://{user}:{password}@db/{db}')
