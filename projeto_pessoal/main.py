from typing import List, Optional
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from models import Cidade, Viagem, Cliente, Reserva

engine = create_engine("sqlite:///bus_website.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sistema de Passagens de Ônibus")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/cidades", response_model=Cidade)
def criar_cidade(cidade: Cidade):
    with Session(engine) as session:
        session.add(cidade)
        session.commit()
        session.refresh(cidade)
        return cidade

@app.get("/cidades", response_model=List[Cidade])
def listar_cidades():
    with Session(engine) as session:
        cidades = session.exec(select(Cidade)).all()
        return cidades

@app.post("/viagens", response_model=Viagem)
def criar_viagem(viagem: Viagem):
    with Session(engine) as session:
        # Checar se origem e destino existem
        origem = session.get(Cidade, viagem.origem_id)
        destino = session.get(Cidade, viagem.destino_id)
        if not origem or not destino:
            raise HTTPException(status_code=404, detail="Cidade de origem ou destino não encontrada")
        session.add(viagem)
        session.commit()
        session.refresh(viagem)
        return viagem

@app.get("/viagens", response_model=List[Viagem])
def listar_viagens(origem_id: Optional[int] = None, destino_id: Optional[int] = None):
    with Session(engine) as session:
        query = select(Viagem)
        if origem_id:
            query = query.where(Viagem.origem_id == origem_id)
        if destino_id:
            query = query.where(Viagem.destino_id == destino_id)
        viagens = session.exec(query).all()
        return viagens

@app.post("/clientes", response_model=Cliente)
def criar_cliente(cliente: Cliente):
    with Session(engine) as session:
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes():
    with Session(engine) as session:
        clientes = session.exec(select(Cliente)).all()
        return clientes

@app.post("/reservas", response_model=Reserva)
def criar_reserva(reserva: Reserva):
    with Session(engine) as session:
        viagem = session.get(Viagem, reserva.viagem_id)
        cliente = session.get(Cliente, reserva.cliente_id) if reserva.cliente_id else None

        if not viagem:
            raise HTTPException(status_code=404, detail="Viagem não encontrada")
        if reserva.cliente_id and not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        assento_ocupado = session.exec(
            select(Reserva).where(Reserva.viagem_id == reserva.viagem_id, Reserva.assento == reserva.assento)
        ).first()
        if assento_ocupado:
            raise HTTPException(status_code=400, detail="Assento já reservado")

        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return reserva

@app.get("/reservas", response_model=List[Reserva])
def listar_reservas(viagem_id: Optional[int] = None, cliente_id: Optional[int] = None):
    with Session(engine) as session:
        query = select(Reserva)
        if viagem_id:
            query = query.where(Reserva.viagem_id == viagem_id)
        if cliente_id:
            query = query.where(Reserva.cliente_id == cliente_id)
        reservas = session.exec(query).all()
        return reservas