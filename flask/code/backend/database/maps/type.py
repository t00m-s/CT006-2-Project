from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)

    # Volendo possiamo settare la size della string
    name = Column(String, nullable=False)
    projects = Relationship("Project", back_populates='type')

    def __repr__(self):
        return f"<Type(id={self.id}, " \
               f"name={self.name})>"
