import html

from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.sql import text
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from .project import Project
from .user import User

Base = declarative_base()


class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    id_project = Column(Integer, ForeignKey(Project.id), nullable=False)
    id_user = Column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
        comment="User that sent the message",
    )
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())

    sender = Relationship(User, back_populates="has_sent")
    project = Relationship(Project, back_populates="messages")

    def getFormattedDate(self):
        if self.created_at is None or self.created_at == '':
            return ''
        return self.created_at.strftime("%d/%m/%Y %H:%M")

    def set_message(self):
        self.message = html.escape(self.message)

    def get_message(self):
        self.message = html.unescape(self.message)


User.has_sent = relationship(Chat, back_populates="sender")

Project.messages = relationship(Chat, back_populates="project")


def my_before_insert_listener_project(mapper, connection, target: Chat):
    target.set_message()


event.listen(Chat, "before_insert", my_before_insert_listener_project)
event.listen(Chat, "before_update", my_before_insert_listener_project)

"""
LA CHAT E' SUL SINGOLO PROGETTO, OGNI PROGETTO PUò AVERE AL MASSIMO UNA SOLA CHAT (o non averne)

I PARTECIPANTI DELLA CHAT, OVVERO COLORO CHE POSSONO SCRIVERE SONO: 
    -L'AUTORE DEL PROGETTO
    -CHIUNQUE ABBIA FATTO ALMENO UNA PROJECT HISTORY (COME REVIEWER)
(#TODO: TRIGGER CHE CONTROLLA CHE ALMENO UNA DI QUESTE DUE CONDIZIONI SIA VERA PER POTER INSERIRE UNA RIGA) 
    
    
TUTTI REVIEWER POSSONO LEGGERE DA TUTTE LE CHAT, POSSONO SCRIVERE SOLO DOPO CHE HANNO CREATO ALMENO UNA PROJECT_HISTORY
OVVIAMENTE I NON REVIWER (AUTORI) POSSONO VEDERE SOLO LE CHAT DEI PROPRI PROGETTI    
IL TESTO DI UN MESSAGGIO E' DI MAX 255 CARATTERI 

"""
