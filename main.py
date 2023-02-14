from typing import Optional, Union
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

# note: normally you'd want to use migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_tickets = db.query(models.Ticket).count()
    tickets = [{
            "id": "1",
            "title": "refaktor atributu jako priprava na db",
            "description": "1. Udelej kontrolu atributu u vsech ras a dodelej refactoring jako pripravu na DB",
            "done": False,
            "priority": 2,
    }]
    if num_tickets == 0:  
        for ticket in tickets:
            db.add(models.Ticket(**ticket))
        db.commit()
    else:
         print(f"{tickets} tickets already in DB")

@app.get('/index/', response_class=HTMLResponse)
async def Index(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)
): #hx_request

    tickets = db.query(models.Ticket).all()
    print(tickets)
    context = {"request": request, "tickets": tickets}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)
