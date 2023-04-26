from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # tabella = classe che eredita da Base


class Role(Base):
    __tablename__ = 'Role'  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_reviewer = Column(Boolean)

    # configuro le relationship e la politica di cascading
    users = relationship("User", back_populates='role')

    def __repr__(self):
        return "<Role(id='%d', name='%s',is_reviewer='%r')>" % (self.id, self.name, self.is_reviewer)
