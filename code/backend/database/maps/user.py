from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .role import *
import hashlib

from flask_login import *

Base = declarative_base()  # tabella = classe che eredita da Base


class User(Base):
    __tablename__ = 'users'  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id_role = Column(Integer, ForeignKey(Role.id), nullable=False)
    birth_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=func.now())
    # configuro le relationship e la politica di cascading
    role = relationship(Role, back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}," \
               f"name={self.name}," \
               f"surname={self.surname}," \
               f"email={self.email}," \
               f"id_role={self.id_role}," \
               f"birth_date={self.birth_date})>"

    """
    Questi metodi vengono eseguiti per far si che quando vado a salvare i dati, siano nel formato desiderato
    Grazie all'event (settato dopo aver definito la classe) li uso
    """

    def set_name(self):
        self.name = self.name.title()

    def set_surname(self):
        self.surname = self.surname.title()

    def set_email(self):
        self.email = self.email.lower()

    def set_password(self):
        hash_object = hashlib.sha512(self.password.encode('utf-8'))
        self.password = hash_object.hexdigest()


Role.users = relationship(User, back_populates='role')


def my_before_insert_listener(mapper, connection, target: User):
    target.set_name()
    target.set_surname()
    target.set_email()
    target.set_password()


event.listen(User, 'before_insert', my_before_insert_listener)
