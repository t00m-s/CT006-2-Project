from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .role import *
from .type import *
from flask_login import UserMixin, login_manager

from ..session import get_session
import hashlib

Base = declarative_base()  # tabella = classe che eredita da Base


class User(Base, UserMixin):
    __tablename__ = "users"  # obbligatorio
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id_role = Column(Integer, ForeignKey(Role.id), nullable=False)
    birth_date = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )
    ban = Column(Boolean, nullable=False, default=True)
    # configuro le relationship e la politica di cascading
    role = relationship(Role, back_populates="users")

    def __repr__(self):
        return (
            f"<User(id={self.id},"
            f"name={self.name},"
            f"surname={self.surname},"
            f"email={self.email},"
            f"id_role={self.id_role},"
            f"birth_date={self.birth_date})>"
        )

    def isReviewer(self):
        return self.role.is_reviewer

    def isAdmin(self):
        return self.id_role == 1

    def getNascita(self):
        if self.birth_date is None or self.birth_date == '':
            return ''
        return self.birth_date.strftime("%d/%m/%Y")

    # region setter
    """
    
    Questi metodi vengono eseguiti per far si che quando vado a salvare i dati
    essi siano nel formato desiderato
    Grazie all'event (settato dopo aver definito la classe) li uso
    """

    def set_name(self):
        self.name = self.name.title()

    def set_surname(self):
        self.surname = self.surname.title()

    def set_email(self):
        self.email = self.email.lower()

    def set_password(self):
        hash_object = hashlib.sha512(self.password.encode("utf-8"))
        self.password = hash_object.hexdigest()

    def set_role(self):
        if (
                self.id_role is None
        ):  # nel caso in cui non sto impostando nessun valore, di default sarà un ricercatore
            self.id_role = get_session().query(Role).filter(Role.is_reviewer == False).first().id
        else:
            self.id_role = self.id_role

    # endregion


Role.users = relationship(User, back_populates="role")


def my_before__update__listener(mapper, connection, target: User):
    target.set_name()
    target.set_surname()
    target.set_email()
    target.set_role()


def my_before__real__insert_listener(mapper, connection, target: User):
    target.set_password()
    target.set_name()
    target.set_surname()
    target.set_email()
    target.set_role()


event.listen(User, "before_insert", my_before__real__insert_listener)
event.listen(User, "before_update", my_before__update__listener)
