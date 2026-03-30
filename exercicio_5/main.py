from fastapi import FastAPI, Request, Response, Depends, Cookie, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users_db = []

class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str | None = None #optional

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
@app.post("/users")
def create_user(user: Usuario):
    users_db.append(user.dict())
    return {"msg": "Usuário criado"}

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.post("/login")
def login(user: Usuario, response: Response):
    user_found = next(
        (u for u in users_db if u["nome"] == user.nome and u["senha"] == user.senha),
        None
    )

    if not user_found:
        raise HTTPException(status_code=401, detail="login invalid")

    # cookie
    response.set_cookie(key="session_user", value=user.nome)
    return {"msg": "Logado com sucesso"}

def get_current_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="nao logado")

    user = next((u for u in users_db if u["nome"] == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sesso invalida")

    return user

@app.get("/home")
def home(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={"user": user}
    )