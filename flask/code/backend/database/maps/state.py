from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()  # tabella = classe che eredita da Base


class State(Base):
    __tablename__ = 'State'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_closed = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now())

    '''
    Non sono sicuro che sia %c per stampare
    '''
    def __repr__(self):
        return "<State(id='%d', name='%s', is_closed='%r', created_at='%c)>" % \
            (self.id, self.name, self.is_closed, self.created_at)
