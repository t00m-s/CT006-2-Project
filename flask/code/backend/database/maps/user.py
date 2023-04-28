from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .role import Role
Base = declarative_base()  # tabella = classe che eredita da Base


class User(Base):
    __tablename__ = 'User'  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    id_role = Column(Integer, ForeignKey(Role.id))
    birth_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=func.now())
    # configuro le relationship e la politica di cascading
    role = relationship("Role", back_populates='users')
    projects = relationship("Project", back_populates='project')

    def __repr__(self):
        return f"<User(id={self.id}," \
               f"name={self.name}," \
               f"surname={self.surname}," \
               f"email={self.email}," \
               f"id_role={self.id_role}," \
               f"birth_date={self.birth_date})>"
