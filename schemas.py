from datetime import datetime, time
from os import truncate
import string
from typing import List, Optional

from pydantic import BaseModel


class MailingListBase(BaseModel):
    text: str = None
    tag: str = None
    start: datetime = None
    end: datetime = None

    class Config:
        orm_mode = True


class MailingListBaseData(MailingListBase):
    id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    phone_number: int
    tag: str = None
    time_zone: str = None

    class Config:
        orm_mode = True


class ClientBaseData(ClientBase):
    id: int

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    id: int
    start: datetime
    status: str
    mailing_list_id: Optional[List[MailingListBase]]
    client_id: Optional[List[ClientBase]]

    class Config:
        orm_mode = True