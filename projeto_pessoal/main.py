from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import SQLModel, Session, create_engine, select
from models import Cidade, Viagem, Cliente, Reserva
from fastapi.templating import Jinja2Templates
import random
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
import math

engine = create_engine("sqlite:///bus_website.db")
templates = Jinja2Templates(directory="templates")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Sistema de Passagens Trip Bus")

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
        for i in range(1000):
            origem, destino = random.sample(cidades_db, 2)

            distancia = calcular_distancia(
                origem.latitude, origem.longitude, 
                destino.latitude, destino.longitude
            )

            custo_por_km = 0.3 
            taxa_fixa = 15.00
            preco = taxa_fixa + (distancia * custo_por_km)

            minutos = random.randint(1, 7*24*60) 

            horario = datetime.now() + timedelta(minutes=minutos)

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

def calcular_distancia(lat1, lon1, lat2, lon2):
    # Raio da Terra em quilômetros
    R = 6371.0
    
    # Convercao graus para radianos
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    cliente_id = request.cookies.get("cliente_id")
    if not cliente_id:
        return RedirectResponse(url="/login") # Para esse projeto simples apenas essa pagina sera redirecionada ao login
    
    return templates.TemplateResponse(request=request, name="index.html", context={})

@app.get("/cidades", response_class=HTMLResponse)
def listar_cidades(request: Request):
    with Session(engine) as session:
        statement = select(Cidade).order_by(Cidade.nome)
        cidades = session.exec(statement).all()
        
    return templates.TemplateResponse(
        request=request,
        name="cidades_options.html",
        context={"cidades": cidades}
    )

@app.get("/viagens", response_class=HTMLResponse)
def listar_viagens(request: Request, origem_id: Optional[str] = None, destino_id: Optional[str] = None):
    with Session(engine) as session:
        query = select(Viagem)
        
        # String para lidar com vazio.
        if origem_id and origem_id.strip():
            query = query.where(Viagem.origem_id == int(origem_id))
            
        if destino_id and destino_id.strip():
            query = query.where(Viagem.destino_id == int(destino_id))
        
        viagens = session.exec(query).all()
        
        for v in viagens:
            _ = v.origem #Lazy loading forca isso
            _ = v.destino

        viagens_ordenadas = sorted(viagens, key=lambda x: x.horario)

    return templates.TemplateResponse(
        request=request, 
        name="viagens_list.html", 
        context={"viagens": viagens_ordenadas}
    )

@app.get("/clientes", response_class=HTMLResponse) # Para teste de desenvolvimento
def listar_clientes(request: Request):
    with Session(engine) as session:
        clientes = session.exec(select(Cliente)).all()
    return templates.TemplateResponse(request=request, name="clientes_list.html", context={"clientes": clientes})


@app.post("/reservas", response_class=HTMLResponse)
def criar_reserva(request: Request, viagem_id: int = Form(...), assento: int = Form(...)):
    if assento < 1:
        return HTMLResponse(content="<p style='color:red;'>Erro: O número da poltrona deve ser 1 ou maior</p>", status_code=400)
    
    with Session(engine) as session:
        viagem = session.get(Viagem, viagem_id)
        cliente_id = request.cookies.get("cliente_id")
        
        if not cliente_id:
            raise HTTPException(status_code=400, detail="Não logado")
        
        
        cliente = session.get(Cliente, int(cliente_id))

        assento_ocupado = session.exec(
            select(Reserva).where(Reserva.viagem_id == viagem_id, Reserva.assento == assento)
        ).first()

        if assento_ocupado:
            return HTMLResponse(content=f"""
                <div style="
                    background: #fdf2f2; 
                    color: #e74c3c; 
                    padding: 10px; 
                    border-radius: 8px; 
                    border: 1px solid #fababa;
                    font-weight: bold;
                    text-align: center;
                    margin-top: 10px;
                ">
                    ❌ Poltrona {assento_ocupado.assento} já está Reservada!
                    <br>
                    <button hx-get="/viagens" hx-target="#resultado-busca" 
                            style="background: none; border: underline; color: #333; cursor: pointer; font-size: 0.8rem;">
                        Tentar Outra poltrona
                    </button>
                </div>
            """)

        reserva = Reserva(viagem_id=viagem_id, assento=assento, cliente_id=cliente.cliente_id)
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        
        _ = reserva.viagem.origem #Lazy loading forca isso
        _ = reserva.viagem.destino
        _ = reserva.cliente

    return templates.TemplateResponse(
        request=request, 
        name="reserva_item.html", 
        context={"reserva": reserva}
    )

@app.get("/reservas", response_class=HTMLResponse)
def listar_reservas(request: Request, viagem_id: Optional[int] = None, cliente_id: Optional[int] = None):
    with Session(engine) as session:
        query = select(Reserva)
        
        cliente_id = request.cookies.get("cliente_id")
        if not cliente_id:
            raise HTTPException(status_code=400, detail="Não logado")

        query = query.where(Reserva.cliente_id == int(cliente_id))
            
        reservas = session.exec(query).all()
        
        for r in reservas: #Lazy loading forca isso
            _ = r.viagem.origem
            _ = r.viagem.destino
            _ = r.cliente
            
    return templates.TemplateResponse(
        request=request, 
        name="reservas_list.html", 
        context={"reservas": reservas}
    )

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
    
    response = Response(content="Sucesso", status_code=200)
    
    response.set_cookie(
        key="cliente_id", 
        value=str(cliente.cliente_id),
        httponly=True
    )
    
    response.headers["HX-Redirect"] = "/"     
    return response 


@app.delete("/reservas/{reserva_id}")
def cancelar_reserva(reserva_id: int):
    with Session(engine) as session:
        reserva = session.get(Reserva, reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva não encontrada")
        
        session.delete(reserva) 
        session.commit()
    
    return Response(status_code=200)

@app.put("/reservas/{reserva_id}", response_class=HTMLResponse)
def atualizar_reserva(request: Request, reserva_id: int, novo_assento: int = Form(...)):
    with Session(engine) as session:
        reserva = session.get(Reserva, reserva_id)
        if not reserva:
            raise HTTPException(status_code=404)

        ocupado = session.exec(
            select(Reserva).where(
                Reserva.viagem_id == reserva.viagem_id, 
                Reserva.assento == novo_assento,
                Reserva.reserva_id != reserva_id
            )
        ).first()

        if ocupado:
            return templates.TemplateResponse(request=request, name="reserva_item.html", context={"reserva": reserva})

        reserva.assento = novo_assento
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        
        _ = reserva.viagem.origem
        _ = reserva.viagem.destino
        _ = reserva.cliente

    return templates.TemplateResponse(
        request=request, 
        name="reserva_item.html", 
        context={"reserva": reserva}
    )

@app.get("/reset") # Usado para desenvolvimento local em testes de cookies
def reset():
    response = RedirectResponse(url="/login")
    response.delete_cookie("cliente_id")
    return response
