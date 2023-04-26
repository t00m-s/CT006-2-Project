from ..engine import *


engine = get_engine()

Base = declarative_base()  # tabella = classe che eredita da Base
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'User'  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    password = Column(String)
    id_role = Column(Integer, ForeignKey(Role.id))


    # configuro le relationship e la politica di cascading
    role = relationship("Role", back_populates='users')

    def __repr__(self):
        return "<Role(id='%d', name='%s', surname='%s',email='%s',password='%s',id_role='%d')>" % \
            (self.id, self.name,self.surname,self.email,self.password,self.id_role)



Base.metadata.create_all(engine)

