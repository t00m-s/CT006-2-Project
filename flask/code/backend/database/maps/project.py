from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .user import User
from .type import Type

Base = declarative_base()  # tabella = classe che eredita da Base


class Project(Base):
    __tablename__ = 'Project'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    id_type = Column(Integer, ForeignKey(Type.id), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="projects")
    type = relationship("Type", back_populates="projects")
    '''
    Non metto description nella stringa
    per comodità
    '''

    def __repr__(self):
        return f"<Type(id={self.id}, " \
               f"id_user={self.id_user}, " \
               f"id_type={self.id_type}, " \
               f"name={self.name}, " \
               f"created_at={self.created_at})>"
