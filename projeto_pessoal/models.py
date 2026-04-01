from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Cidade(SQLModel, table=True):
    cidade_id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    latitude: float
    longitude: float

    viagens_origem: List["Viagem"] = Relationship(
        back_populates="origem", sa_relationship_kwargs={"foreign_keys": "[Viagem.origem_id]"}
    )
    viagens_destino: List["Viagem"] = Relationship(
        back_populates="destino", sa_relationship_kwargs={"foreign_keys": "[Viagem.destino_id]"}
    )

class Cliente(SQLModel, table=True):
    cliente_id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    contato: str

    reservas: List["Reserva"] = Relationship(back_populates="cliente")

class Viagem(SQLModel, table=True):
    viagem_id: Optional[int] = Field(default=None, primary_key=True)
    origem_id: int = Field(foreign_key="cidade.cidade_id")
    destino_id: int = Field(foreign_key="cidade.cidade_id")
    horario: str
    preco: float

    origem: Optional[Cidade] = Relationship(
        back_populates="viagens_origem", sa_relationship_kwargs={"foreign_keys": "[Viagem.origem_id]"}
    )
    destino: Optional[Cidade] = Relationship(
        back_populates="viagens_destino", sa_relationship_kwargs={"foreign_keys": "[Viagem.destino_id]"}
    )
    reservas: List["Reserva"] = Relationship(back_populates="viagem")

class Reserva(SQLModel, table=True):
    reserva_id: Optional[int] = Field(default=None, primary_key=True)
    viagem_id: int = Field(foreign_key="viagem.viagem_id")
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.cliente_id")
    assento: int

    viagem: Optional[Viagem] = Relationship(back_populates="reservas")
    cliente: Optional[Cliente] = Relationship(back_populates="reservas")