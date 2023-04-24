from ..engine import *

engine = get_engine()

Base = declarative_base()  # tabella = classe che eredita da Base
Session = sessionmaker(pbind=engine)
session = Session()


class Role(Base):
    __tablename__ = 'Role'  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_reviewer = Column(Boolean)

    # configuro le relationship e la politica di cascading
    users = relationship("User", back_populates='role')

    def __repr__(self):
        return "<Product(maker='%s', model='%d',type='%s')>" % (self.maker, self.model, self.type)
