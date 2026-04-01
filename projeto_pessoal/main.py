from fastapi import FastAPI
from sqlmodel import Session, select, SQLModel, create_engine

from models import Cidade

engine = create_engine("sqlite:///bus_website.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/cidades")
def criar_cidade(cidade: Cidade):
    with Session(engine) as session:
        session.add(cidade)
        session.commit()
        return cidade


@app.get("/cidades")
def listar_cidades():
    with Session(engine) as session:
        return session.exec(select(Cidade)).all()
