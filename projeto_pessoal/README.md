# Sistema de Busca de Passagens de Ônibus

Este projeto será uma aplicação web simples fullstack, desenvolvida para disciplina MAC0350 na USP. A ideia do sistema é permitir que um usuário busque viagens de ônibus entre cidades, visualize horários disponíveis e registre reservas de assentos, além de rotas de forma eficiente. O sistema foi pensado para rodar localmente e integrar um frontend, um backend e um banco de dados.

O frontend da aplicação será construído usando HTML, CSS e JavaScript. O backend será implementado em Python usando FastAPI, o que permite criar rotas e endpoints para comunicação com o frontend. Para persistência de dados é utilizado um banco de dados SQL, provavelmente o SQLModel para modelar as tabelas e facilitar a interação com o banco.

A aplicação possui funcionalidades simples, como buscar viagens entre cidades, visualizar horários disponíveis, registrar uma reserva de assento e listar reservas que já foram feitas.

A estrutura do projeto está organizada em algumas pastas principais. Existe uma pasta de frontend contendo os arquivos HTML, CSS e JavaScript responsáveis pela interface do usuário. Terá também uma pasta de backend onde ficam os arquivos Python que definem a API, os modelos de dados e a configuração do banco. Também há uma configuração de Docker para facilitar a execução da aplicação localmente.

Exemplo simplificado da estrutura do projeto:

    bus-pass-system/

    frontend/
        index.html
        buscar.html
        reservas.html
        styles.css
        script.js

    backend/
        main.py
        models.py
        database.py

    docker/
        docker-compose.yml

    README.md

O banco de dados do sistema é composto por três tabelas principais. Uma tabela de cidades, contendo um identificador e o nome da cidade. Uma tabela de viagens, contendo informações como origem, destino, horário e preço da viagem. E uma tabela de reservas, que registra qual viagem foi reservada, o nome do passageiro e o número do assento. Talvez seja adicionada uma tabela de clientes.

Para executar o projeto localmente é necessário clonar o repositório e iniciar a aplicação. Primeiro, clone o repositório:

git clone git@github.com:MikeFutorny/MAC0350-Desenvolvimento-de-Sistemas-de-Software.git

Depois entre na pasta do projeto:

cd bus-pass-system

Antes de executar o backend é necessário instalar as dependências do projeto. Isso pode ser feito com:

pip install -r requirements.txt

Após isso, o projeto pode ser iniciado utilizando Docker com o comando:

docker compose up

Isso irá iniciar os serviços necessários para rodar a aplicação localmente.

Este projeto foi desenvolvido como prática para consolidar conhecimentos em HTML, CSS, JavaScript, manipulação da DOM, criação de APIs com FastAPI, integração com banco de dados SQL e uso de Docker para executar aplicações localmente.

## Autor

Mikhail Futorny

Projeto desenvolvido como exercício de aprendizado em desenvolvimento web - discplina MAC0350.