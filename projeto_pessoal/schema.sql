CREATE TABLE cidade (
    cidade_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

CREATE TABLE cliente (
    cliente_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    contato TEXT NOT NULL
);

CREATE TABLE viagem (
    viagem_id INTEGER PRIMARY KEY,
    origem_id INTEGER NOT NULL,
    destino_id INTEGER NOT NULL,
    horario TEXT NOT NULL,
    preco REAL NOT NULL,

    FOREIGN KEY (origem_id) REFERENCES cidade(cidade_id),
    FOREIGN KEY (destino_id) REFERENCES cidade(cidade_id)
);

CREATE TABLE reserva (
    reserva_id INTEGER PRIMARY KEY,    
    viagem_id INTEGER NOT NULL,
    cliente_id INTEGER,
    assento INTEGER NOT NULL,

    FOREIGN KEY (viagem_id) REFERENCES viagem(viagem_id),
    FOREIGN KEY (cliente_id) REFERENCES cliente(cliente_id)
);