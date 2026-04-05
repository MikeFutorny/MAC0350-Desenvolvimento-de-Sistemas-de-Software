from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Session, create_engine, select
from models import Cidade, Viagem, Cliente, Reserva
from fastapi.templating import Jinja2Templates

engine = create_engine("sqlite:///bus_website.db")
templates = Jinja2Templates(directory="templates")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sistema de Passagens de Bus")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.post("/cidades", response_class=HTMLResponse)
def criar_cidade(request: Request, nome: str = Form(...), latitude: float = Form(...), longitude: float = Form(...)):
    cidade = Cidade(nome=nome, latitude=latitude, longitude=longitude)
    with Session(engine) as session:
        session.add(cidade)
        session.commit()
        session.refresh(cidade)
    return templates.TemplateResponse(request=request, name="cidade_item.html", context={"cidade": cidade})

@app.get("/cidades", response_class=HTMLResponse)
def listar_cidades(request: Request):
    with Session(engine) as session:
        cidades = session.exec(select(Cidade)).all()
    return templates.TemplateResponse(request=request, name="cidades_list.html", context={"cidades": cidades})

@app.post("/viagens", response_class=HTMLResponse)
def criar_viagem(request: Request, origem_id: int = Form(...), destino_id: int = Form(...), horario: str = Form(...), preco: float = Form(...)):
    with Session(engine) as session:
        origem = session.get(Cidade, origem_id)
        destino = session.get(Cidade, destino_id)
        if not origem or not destino:
            raise HTTPException(status_code=404, detail="Cidade de origem ou destino não encontrada")
        viagem = Viagem(origem_id=origem_id, destino_id=destino_id, horario=horario, preco=preco)
        session.add(viagem)
        session.commit()
        session.refresh(viagem)
    return templates.TemplateResponse(request=request, name="viagem_item.html", context={"viagem": viagem})

@app.get("/viagens", response_class=HTMLResponse)
def listar_viagens(request: Request, origem_id: Optional[int] = None, destino_id: Optional[int] = None):
    with Session(engine) as session:
        query = select(Viagem)
        if origem_id:
            query = query.where(Viagem.origem_id == origem_id)
        if destino_id:
            query = query.where(Viagem.destino_id == destino_id)
        viagens = session.exec(query).all()
    return templates.TemplateResponse(request=request, name="viagens_list.html", context={"viagens": viagens})

@app.post("/clientes", response_class=HTMLResponse)
def criar_cliente(request: Request, nome: str = Form(...), contato: str = Form(...)):
    cliente = Cliente(nome=nome, contato=contato)
    with Session(engine) as session:
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
    return templates.TemplateResponse(request=request, name="cliente_item.html", context={"cliente": cliente})

@app.get("/clientes", response_class=HTMLResponse)
def listar_clientes(request: Request):
    with Session(engine) as session:
        clientes = session.exec(select(Cliente)).all()
    return templates.TemplateResponse(request=request, name="clientes_list.html", context={"clientes": clientes})

@app.post("/reservas", response_class=HTMLResponse)
def criar_reserva(request: Request, viagem_id: int = Form(...), assento: int = Form(...), cliente_id: Optional[int] = Form(None)):
    with Session(engine) as session:
        viagem = session.get(Viagem, viagem_id)
        cliente = session.get(Cliente, cliente_id) if cliente_id else None
        if not viagem:
            raise HTTPException(status_code=404, detail="Viagem não encontrada")
        if cliente_id and not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        assento_ocupado = session.exec(
            select(Reserva).where(Reserva.viagem_id == viagem_id, Reserva.assento == assento)
        ).first()
        if assento_ocupado:
            raise HTTPException(status_code=400, detail="Assento já reservado")
        reserva = Reserva(viagem_id=viagem_id, assento=assento, cliente_id=cliente_id)
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
    return templates.TemplateResponse(request=request, name="reserva_item.html", context={"reserva": reserva})

@app.get("/reservas", response_class=HTMLResponse)
def listar_reservas(request: Request, viagem_id: Optional[int] = None, cliente_id: Optional[int] = None):
    with Session(engine) as session:
        query = select(Reserva)
        if viagem_id:
            query = query.where(Reserva.viagem_id == viagem_id)
        if cliente_id:
            query = query.where(Reserva.cliente_id == cliente_id)
        reservas = session.exec(query).all()
    return templates.TemplateResponse(request=request, name="reservas_list.html", context={"reservas": reservas})