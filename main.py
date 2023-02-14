from typing import Optional, Union, List
from fastapi import FastAPI, Request, Header, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc

from schemas import Item, ItemCreate
from crud import get_ticket, create_db_ticket
from database import SessionLocal, engine
from models import Ticket
import models
import pathlib
import json

# note: normally you'd want to use migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

data =[]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: jak logovat chybove udalosti - jak catchnout exceptiony?
# @app.on_event("shutdown")
# def shutdown_event():
#     with open("log.txt", mode="a") as log:
#         log.write("\nApplication shutdown")

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_tickets = db.query(models.Ticket).count()

# TODO: log
    # with open("log.txt", mode="a") as log:
    #     log.write("\nApplication startup")

    tickets = [{
            "id": 3,
            "title": "refaktor asadfasdfas atributu jako priprava na db",
            "description": "1. Udelej kontrolu atributu u vsech ras a dodelej refactoring jako pripravu na DB",
            "done": False,
            "priority": 2,
    },
    {
            "id": 4,
            "title": "for test",
            "description": "test sdfgsdfg description",
            "done": True,
            "priority": 3,
    },
    {
            "id": 5,
            "title": "refaktor atributu sdfgsdfgsd jako priprava na db",
            "description": "1. Udelej kontrolu atributu u vsech ras a dodelej refactoring jako pripravu na DB",
            "done": False,
            "priority": 2,
    },
    {
            "id": 6,
            "title": "for sdfgsdfgsdfg test",
            "description": "test sdfgsdfgsdf description",
            "done": True,
            "priority": 3,
    }
    ]
    if num_tickets == 0:  
        for ticket in tickets:
            db.add(models.Ticket(**ticket))
        db.commit()
    else:
         print(f"{num_tickets} tickets already in DB")
    
    datapath = pathlib.Path() / 'data' / 'tickets.json'
    with open(datapath, 'r') as f:
        tickets = json.load(f)
        for ticket in tickets:
            data.append(models.Ticket(**ticket))
    db.commit()
    print(f"{num_tickets} tickets already in DB")

@app.get('/index/', response_class=HTMLResponse)
async def GetALL_paging(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db), 
    page: int = 1
): #hx_request
    N = 2
    OFFSET = (page - 1) * N
    tickets = db.query(models.Ticket).offset(OFFSET).limit(N)
    # tickets = db.query(models.Ticket).all()
    context = {"request": request, "tickets": tickets, "page": page}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)

# TODO: response model co dela ???
@app.get("/index/{tickets_id}", response_model=Item)
def get_tickets_by_id(tickets_id: int, response: Response) -> Item:
    # finds tickets by id
    db = SessionLocal()
    ticket = get_ticket(db, tickets_id)
    if ticket is None:
        response.status_code = 404
        return "Ticket not found"
    return ticket


@app.put("/index/{create_ticket}", response_model=ItemCreate)
def add_ticket(
    title: str,
    description: str,
    done: bool, 
    priority: int,
    response: Response
    ) -> ItemCreate:
    # add ticket
    db = SessionLocal()

    # TODO: jak se veme posledni id zaznamu a pripocita +1, jak se z ticketu udela dict?
    id = (db.query(models.Ticket).order_by(desc(Ticket.id)).first())
    id.id = id.id + 1
    print(f"TOTO JE ID: {id.id}")
    ticket = create_db_ticket(
        db, 
        # id = id.id, 
        title = id.title,
        description = id.description,
        done = id.done,
        priority = id.priority
        )
    return ticket
