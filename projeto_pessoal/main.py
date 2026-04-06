from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import SQLModel, Session, create_engine, select
from models import Cidade, Viagem, Cliente, Reserva
from fastapi.templating import Jinja2Templates
import random
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles


engine = create_engine("sqlite:///bus_website.db")
templates = Jinja2Templates(directory="templates")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sistema de Passagens de Bus")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    seed_inicial_db()


def seed_inicial_db():
    with Session(engine) as session:
        cidades_existentes = session.exec(select(Cidade)).first()

        if cidades_existentes:
            return # banco ja populado

        cidades = [
            Cidade(nome="São Paulo", latitude=-23.55, longitude=-46.63),
            Cidade(nome="Rio de Janeiro", latitude=-22.90, longitude=-43.17),
            Cidade(nome="Belo Horizonte", latitude=-19.92, longitude=-43.94),
            Cidade(nome="Curitiba", latitude=-25.43, longitude=-49.27),
            Cidade(nome="Florianópolis", latitude=-27.59, longitude=-48.55),
            Cidade(nome="Porto Alegre", latitude=-30.03, longitude=-51.23),
            Cidade(nome="Brasília", latitude=-15.78, longitude=-47.93),
            Cidade(nome="Salvador", latitude=-12.97, longitude=-38.50),
            Cidade(nome="Recife", latitude=-8.05, longitude=-34.88),
            Cidade(nome="Fortaleza", latitude=-3.73, longitude=-38.52),
            Cidade(nome="Manaus", latitude=-3.10, longitude=-60.02),
            Cidade(nome="Belém", latitude=-1.45, longitude=-48.50),
            Cidade(nome="Goiânia", latitude=-16.68, longitude=-49.25),
            Cidade(nome="Campinas", latitude=-22.90, longitude=-47.06),
            Cidade(nome="Santos", latitude=-23.96, longitude=-46.33),
            Cidade(nome="Ribeirão Preto", latitude=-21.17, longitude=-47.81),
            Cidade(nome="São José dos Campos", latitude=-23.18, longitude=-45.88),
            Cidade(nome="Uberlândia", latitude=-18.91, longitude=-48.27),
            Cidade(nome="Londrina", latitude=-23.30, longitude=-51.16),
            Cidade(nome="Maringá", latitude=-23.42, longitude=-51.93),
            Cidade(nome="Joinville", latitude=-26.30, longitude=-48.85),
            Cidade(nome="Blumenau", latitude=-26.92, longitude=-49.07),
            Cidade(nome="Vitória", latitude=-20.31, longitude=-40.33),
            Cidade(nome="Natal", latitude=-5.79, longitude=-35.21),
            Cidade(nome="João Pessoa", latitude=-7.12, longitude=-34.86),
            Cidade(nome="Maceió", latitude=-9.66, longitude=-35.71),
            Cidade(nome="Aracaju", latitude=-10.91, longitude=-37.07),
            Cidade(nome="Campo Grande", latitude=-20.47, longitude=-54.62),
            Cidade(nome="Cuiabá", latitude=-15.60, longitude=-56.10),
            Cidade(nome="Teresina", latitude=-5.09, longitude=-42.80),
        ]
        session.add_all(cidades)
        session.commit()

        cidades_db = session.exec(select(Cidade)).all()

        viagens = []
        for i in range(100):
            origem, destino = random.sample(cidades_db, 2)

            horas = random.randint(1, 24 * 7) # Ate uma semana de tempo

            horario = datetime.now() + timedelta(hours=horas)

            preco = round(random.uniform(50, 300), 2)

            viagens.append(
                Viagem(
                    origem_id=origem.cidade_id,
                    destino_id=destino.cidade_id,
                    horario=horario.strftime("%Y-%m-%d %H:%M"),
                    preco=preco
                )
            )

        session.add_all(viagens)
        session.commit()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    cliente_id = request.cookies.get("cliente_id")
    if not cliente_id:
        return RedirectResponse(url="/login") # Para esse projeto simples apenas essa pagina sera redirecionada ao login
    
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
    return templates.TemplateResponse(
        request=request,
        name="cidades_options.html",
        context={"cidades": cidades}
    )

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

@app.get("/clientes", response_class=HTMLResponse)
def listar_clientes(request: Request):
    with Session(engine) as session:
        clientes = session.exec(select(Cliente)).all()
    return templates.TemplateResponse(request=request, name="clientes_list.html", context={"clientes": clientes})

@app.post("/reservas", response_class=HTMLResponse)
def criar_reserva(request: Request, viagem_id: int = Form(...), assento: int = Form(...)):
    with Session(engine) as session:
        viagem = session.get(Viagem, viagem_id)

        cliente_id = request.cookies.get("cliente_id")
        if not cliente_id:
            raise HTTPException(status_code=400, detail="Nao Logado")
        cliente_id = int(cliente_id)

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


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

@app.post("/login")
def fazer_login(nome: str = Form(...), contato: str = Form(...)):
    with Session(engine) as session:
        cliente = Cliente(nome=nome, contato=contato)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="cliente_id", value=str(cliente.cliente_id))

    return response

@app.get("/reset") # Para desenvolvimento local
def reset():
    response = RedirectResponse(url="/login")
    response.delete_cookie("cliente_id")
    return response