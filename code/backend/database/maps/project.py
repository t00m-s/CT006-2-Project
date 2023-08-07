from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .user import User
from .type import Type
from ..session import get_session
import html

Base = declarative_base()  # tabella = classe che eredita da Base


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    id_type = Column(Integer, ForeignKey(Type.id), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now(),
                        server_default=func.now())

    user = relationship(User, back_populates="projects")
    type = relationship(Type, back_populates="projects")
    '''
    Non metto description nella stringa
    per comodità
    '''

    def __repr__(self):
        return f"< Project(id={self.id}, name={self.name}, created_at={self.created_at}) >"

    def getTypes(self):
        return get_session().query(Type).join(Project).filter(Project.id == self.id)

    def set_description(self):
        self.description = html.escape(self.description)


User.projects = relationship(Project, back_populates='user')
Type.projects = Relationship(Project, back_populates='type')


def my_before_insert_listener_project(mapper, connection, target: User):
    target.set_description()


event.listen(Project, 'before_insert', my_before_insert_listener_project)
event.listen(Project, 'before_update', my_before_insert_listener_project)
