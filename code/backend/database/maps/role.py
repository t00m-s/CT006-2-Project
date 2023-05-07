from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    is_reviewer = Column(Boolean, nullable=False)

    # configuro le relationship e la politica di cascading

    def __repr__(self):
        return f"<Role(id={self.id}," \
               f"name={self.name}," \
               f"is_reviewer={self.is_reviewer})>"
