from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer,String,
    Float, DateTime, Date
)
from sqlalchemy.orm import relationship

from database import Base

class MailingList(Base):
    __tablename__ = "mailing_list"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    tag = Column(String)
    start = Column(DateTime)
    end = Column(DateTime)

    message = relationship("Message", back_populates="mail_list")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(Integer)
    tag = Column(String)
    time_zone = Column(String)

    message_client = relationship("Message", back_populates="client")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime)
    status = Column(String)
    mailing_list_id = Column(Integer, ForeignKey("mailing_list.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))

    mail_list = relationship("MailingList", back_populates="message")
    client = relationship("Client", back_populates="message_client")