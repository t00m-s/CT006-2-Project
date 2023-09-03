from sqlalchemy import *
from sqlalchemy.sql import text
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from .project import *
from .state import *
from .user import *

Base = declarative_base()


class ProjectHistory(Base):
    __tablename__ = "project_history"
    id = Column(Integer, primary_key=True)
    id_project = Column(Integer, ForeignKey(Project.id), nullable=False)
    id_state = Column(Integer, ForeignKey(State.id), nullable=False)
    id_user_reviewer = Column(Integer, ForeignKey(User.id), nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())

    reviewer = Relationship(User, back_populates="reviewed_histories")
    state = Relationship(State, back_populates="attributed_histories")
    project = Relationship(Project, back_populates="histories")

    def __repr__(self):
        return f"<ProjectHistory(id={self.id}, id_project={self.id_project}, id_state={self.id_state}, created_at={self.created_at})>"

    def isClosed(self):
        return self.state.is_closed


Project.histories = relationship(
    ProjectHistory, back_populates="project", order_by=ProjectHistory.id.desc()
)
User.reviewed_histories = relationship(ProjectHistory, back_populates="reviewer")
State.attributed_histories = relationship(ProjectHistory, back_populates="state")
