from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

#DB em lista
usuarios = []

class User(BaseModel):
    nome: str
    idade: int


@app.delete("/users")
async def delete_users():
    usuarios.clear()
    return {"message": "Todos os users foram removidos"}

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("exercicio_4_index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/users")
async def add_user(user: User):
    usuarios.append(user.dict())
    return {"message": "user adicionado", "users": usuarios}

@app.get("/users")
async def get_users(index: int | None = None):
    if index is not None:
        if 0 <= index < len(usuarios):
            return usuarios[index]
        return {"error": "indice invalido"}
    return usuarios
