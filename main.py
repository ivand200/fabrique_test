from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from fastapi.responses import JSONResponse

import requests
import json
import sys
import logging

import models
from schemas import ClientBase, MessageBase, MailingListBase
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

from config import TOKEN

app = FastAPI()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler_format = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
handler.setFormatter(handler_format)
logger.addHandler(handler)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/test")
async def root():
    logger.info("test")
    return {"message": "Hello World"}


@app.post("/clients/", response_model=ClientBase)
def create_client(client: ClientBase, db: Session = Depends(get_db)):
    """Создание клиента"""
    logger.info("New client: ", client)
    db_user = models.Client(**client.dict())
    db.add(db_user)
    db.commit()
    return db_user


@app.put("/clients/{client_id}", response_model=ClientBase)
def update_client(client_id: int, client: ClientBase, db: Session = Depends(get_db)):
    """Обновление клиента"""
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    logger.info("Update client: ", client.phone_number, client.time_zone, client.tag)
    db_client.phone_number = client.phone_number
    db_client.time_zone = client.time_zone
    db_client.tag = client.tag
    db.commit()
    db.refresh(db_client)
    return db_client


@app.delete("/clients/{client_id}", response_model=ClientBase)
def delete_client(client_id: int, client: ClientBase, db: Session = Depends(get_db)):
    """Удаление клиента"""
    logger.info("Delete client_id: ", client_id)
    db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    db.delete(db_client)
    db.commit()


# @app.post("/mailing_list/", response_model=MailingListBase)
# def create_list(mailing_list: MailingListBase, db: Session = Depends(get_db)):
#     """Создание рассылки"""
#     db_mail = models.MailingList(**mailing_list.dict())
#     db.add(db_mail)
#     db.commit()
#     return db_mail


@app.post("/mail/")
def create_mail(mailing_list: MailingListBase, db: Session = Depends(get_db)):
    """Создание рассылки"""
    db_clients = (
        db.query(models.Client).filter(models.Client.tag == mailing_list.tag).all()
    )
    try:
        for message in db_clients:
            id = message.id
            payload = {
                "id": id,
                "phone": message.phone_number,
                "text": mailing_list.text,
            }
            response = requests.post(
                f"https://probe.fbrq.cloud/v1/send/{id}",
                headers={"Authorization": "Bearer " + TOKEN},
                json=payload,
            )
            logger.info(f"New mail list: {payload}")
        if response.status_code == 200:
            return JSONResponse(status_code=200, content={"result": "OK"})
    except:
        return JSONResponse(
            status_code=400,
            content={"code": 100, "description": {"status": "Внутренняя ошибка"}},
        )


@app.put("/mailing_list/{list_id}", response_model=MailingListBase)
def update_list(list_id: int, list: MailingListBase, db: Session = Depends(get_db)):
    """Обновление рассылки"""
    db_list = (
        db.query(models.MailingList).filter(models.MailingList.id == list_id).first()
    )
    logger.info(f"Update mail list: {list_id}")
    db_list.start = list.start
    db_list.end = list.end
    db_list.text = list.text
    db_list.tag = list.tag
    db.commit()
    db.refresh(db_list)
    return db_list


@app.delete("/mailing_list/{list_id}", response_model=MailingListBase)
def update_list(list_id: int, list: MailingListBase, db: Session = Depends(get_db)):
    """Удаление рассылки"""
    db_mail = (
        db.query(models.MailingList).filter(models.MailingList.id == list_id).first()
    )
    logger.info(f"Delete mail list id: {list_id}")
    db.delete(db_mail)
    db.commit()

