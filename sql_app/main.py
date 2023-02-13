from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/index/', response_class=HTMLResponse)
def Index(request: Request, hx_request: Optional[str] = Header(None)): #hx_request
    tickets=[
        {
            "id": "1",
            "name": "refaktor atributu jako priprava na db",
            "description": "1. Udelej kontrolu atributu u vsech ras a dodelej refactoring jako pripravu na DB",
            "is_done": "false",
            "priority": 2,
        },
        {
            "id": "2",
            "name": "zjisti jak nalivat db - napr pydantic z excelu",
            "description": " 1. poptej se na nejlepsi reseni seniora \n2. rekni mu jak to mas namysleno \n- pydantic a z excelu ci csv, txt... \n3. zkoumej pro a proti ruznych konceptu ze kterych pak migrujes DB",
            "is_done": "false",
            "priority": 1,
        }
    ]
    context = {"request": request, "tickets": tickets}
    if hx_request:
        return templates.TemplateResponse("Partials/table.html", context)
    return templates.TemplateResponse("index.html", context)

