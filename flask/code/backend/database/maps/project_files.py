from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProjectFiles(Base):
    __tablename__ = "Project Files"
    id = Column(Integer, primary_key=True)
    id_project_history = Column(Integer, ForeignKey())
