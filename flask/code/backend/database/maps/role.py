
from ..engine import *


engine = get_engine()

Base = declarative_base()  # tabella = classe che eredita da Base
Session = sessionmaker(bind=engine)
session = Session()


class Role(Base):
    __tablename__ = 'Role'  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_reviewer = Column(Boolean)

    # configuro le relationship e la politica di cascading
    users = relationship("User", back_populates='role')


    def __repr__(self):
        return "<Role(id='%d', name='%s',is_reviewer='%r')>" % (self.id, self.name, self.is_reviewer)



Base.metadata.create_all(engine)



"""
TEST


new_role = Role(name = 'sgrodo', is_reviewer = False)
session.add(new_role)
session.commit()
"""