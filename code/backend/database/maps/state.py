from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from ..session import get_session

Base = declarative_base()  # tabella = classe che eredita da Base


class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    is_closed = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now(),
                        server_default=func.now())

    def __repr__(self):
        return f"<State(id={self.id}," \
               f"name={self.name}," \
               f"is_closed={self.is_closed}," \
               f"created_at={self.created_at})>"

    @staticmethod
    def getSubmittedID():
        return get_session().query(State).filter(State.name == 'Submitted').first().id
