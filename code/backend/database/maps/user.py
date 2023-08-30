from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from .role import *
from .type import *

from ..session import get_session
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
    created_at = Column(DateTime, nullable=False, default=func.now(), server_default=func.now())
    is_authenticated = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    # configuro le relationship e la politica di cascading
    role = relationship(Role, back_populates='users')

    def __repr__(self):
        return f"<User(id={self.id}," \
               f"name={self.name}," \
               f"surname={self.surname}," \
               f"email={self.email}," \
               f"id_role={self.id_role}," \
               f"birth_date={self.birth_date}," \
               f"is_authenticated={self.is_authenticated}," \
               f"is_active={self.is_active} )>"

    # region List of methods useful for login_manager

    def is_active(self):
        """
        Checks if the user can access the site. 
        @params self User
        """
        return self.is_active

    def get_id(self):
        """
        Gets the user id
        @params self User
        """
        return str(self.id)

    def is_anonymous(self):
        """ 
        Needed for flask-login but disabled here because 
        anonymouse users are not supported. 
        @params self User
        """
        return False

    def is_authenticated(self):
        """ 
        Checks if the user is logged in 
        @params self User
        """
        return self.is_authenticated

    def isReviewer(self):
        return self.role.is_reviewer

    # endregion

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
        hash_object = hashlib.sha512(self.password.encode('utf-8'))
        self.password = hash_object.hexdigest()

    def set_role(self):
        if self.id_role is None:  # nel caso in cui non sto impostando nessun valore, di default sarà un ricercatore
            self.id_role = 3  # provvisoriamete metto l'id forzato
            # FIXME self.role = get_session().query(Role).filter_by(name='Researcher').first().id
            # va in errore, penso sia perchè non posso usare la sessione per fare una select finchè ho una sessione per fare l'inser
            # il che mi sembra assurdo
        else:
            self.id_role = self.id_role

    # endregion


Role.users = relationship(User, back_populates='role')


def my_before_insert_listener(mapper, connection, target: User):
    target.set_name()
    target.set_surname()
    target.set_email()
    target.set_password()
    target.set_role()


event.listen(User, 'before_insert', my_before_insert_listener)
event.listen(User, 'before_update', my_before_insert_listener)
