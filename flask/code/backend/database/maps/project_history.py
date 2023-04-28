from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from .project import Project
from .state import State
from .user import User

Base = declarative_base()


class ProjectHistory(Base):
    __tablename__ = 'project_history'
    id = Column(Integer, primary_key=True)
    id_project = Column(Integer, ForeignKey(Project.id), nullable=False)
    id_state = Column(Integer, ForeignKey(State.id), nullable=False)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    note = Column(Text)
    created_at = Column(DateTime, default=func.now())

    reviewer = Relationship('User', back_populates='user')
    state = Relationship('State', back_populates='state')
    project = Relationship('Project', back_populates='project')
    files = Relationship('ProjectFiles', back_populates='project_file')

    def __repr__(self):
        return f"<Project_History(id={self.id}," \
               f"id_project={self.id_project}," \
               f"id_state={self.id_state}," \
               f"id_user={self.id_user}," \
               f"created_at={self.created_at})>"
