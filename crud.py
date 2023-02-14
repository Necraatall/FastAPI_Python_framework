from sqlalchemy.orm import Session
from typing import Union, List
import models, schemas


def get_ticket(db: Session, id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == id).first()


def get_all_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()


# def create_tickets(db: Session, ticket: schemas.ItemCreate, id: int):
#         #     {
#         #     "id": "1",
#         #     "name": "refaktor atributu jako priprava na db",
#         #     "description": "1. Udelej kontrolu atributu u vsech ras a dodelej refactoring jako pripravu na DB",
#         #     "done": "false",
#         #     "priority": 2,
#         # },
#     # last_ticket_id = db.query(models.Ticket).order_by(models.Ticket.id.desc()).first()
#     ticket = models.Ticket(
#         id = ((db.query(models.Ticket).order_by(models.Ticket.id.desc()).first()).id + 1),
#         title = models.Ticket(ticket.title, "DE TO"),
#         description = "Vypada to ze to de",
#         done = False,
#         priority = 3,
#     )
#     db.add(ticket)
#     db.commit()
#     db.refresh(ticket)
#     return ticket

# TODO: dodelat - put , zatim nefunkcni
def update_ticket(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_db_ticket(
    db: Session,
    ticket: schemas.ItemCreate):
    db_ticket = models.Ticket(**ticket.dict(), id=id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item