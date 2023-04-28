from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .project_history import *

Base = declarative_base()


class ProjectFiles(Base):
    __tablename__ = "project_files"
    id = Column(Integer, primary_key=True)
    id_project_history = Column(Integer, ForeignKey(ProjectHistory.id), nullable=False)

    project_history = Relationship('ProjectHistory', back_populates='project_history')
