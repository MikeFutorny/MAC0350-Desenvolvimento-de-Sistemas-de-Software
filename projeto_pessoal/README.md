# Sistema de Busca de Passagens de Ônibus (Trip Bus)

## Overview

Este projeto é uma aplicação web simples fullstack, desenvolvida para disciplina MAC0350 da USP. O sistema Trip Bus permite que um usuário busque viagens de ônibus entre cidades, visualize horários e datas disponíveis e registre reservas de assentos. O sistema tem uma inteligencia de cálculo de custo, assim como assentos reservados, assim como tela de login com cookies. Essa aplicação foi pensada para rodar localmente e integrar o frontend, o backend e o banco de dados. O banco de dados é gerado na primeira vez que um usuário sobe a aplicação em seu computador e persiste após reiniciar programa. A aplicação tem basicamente duas páginas (além do login), a de "Buscar Viagens" que possibilita filtrar por origem e destino e a "Minhas Reservas" que mostra as reservas realizadas. As reservas mostradas nessa aba são apenas aquelas feitas por esse cliente especifico, se alterar o login as reservas vão ser outras, mas o banco persiste as reservas antigas do outro usuário, portanto os mesmos assentos não poderão ser reservados. A interface utiliza HTMX para permitir uma experiência dinâmica e fluida, realizando atualizações parciais do DOM sem a necessidade de recarregar a página a cada interação.


## Estrutura do Projeto
    trip-bus/
    ├── main.py
    ├── models.py
    ├── static/
    │   └── style.css
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── viagens_list.html
    │   ├── reservas_list.html
    │   ├── reserva_item.html
    │   ├── cidades_options.html
    │   └── clientes_list.html
    ├── bus_website.db
    └── README.md

## Backend

O backend foi desenvolvido com FastAPI e SQLModel, utilizando o SQLite para persistência de dados. A lógica principal baseia se em rotas que processam requisições assíncronas e retornam fragmentos de HTML para integração com o HTMX.

Entre os componentes técnicos, o sistema implementa a Fórmula de Haversine para calcular distâncias entre cidades via latitude e longitude, definindo o preço das passagens de forma dinâmica. A gestão de usuários utiliza cookies, vinculando cada reserva ao seu respectivo cliente sem a necessidade de recarregamento total da página. Ao ser iniciado, o sistema executa um seed automático que popula o banco com 30 cidades e suas coordenadas, além de 1.000 viagens geradas aleatoriamente com data em até uma semana, garantindo um ambiente realista.


## Frontend

A interface utiliza o motor de templates Jinja2 com herança de componentes a partir de um layout base. É usado HTMX, que permite atualizações parciais do DOM e buscas assíncronas sem recarregamento da página. Isso proporciona uma experiência fluida de Single Page Application, na qual filtros de busca e confirmações de reserva são injetados instantaneamente na tela. 

## Execução

Para executar o projeto localmente é necessário clonar o repositório e iniciar a aplicação. Primeiro, clone o repositório:

git clone git@github.com:MikeFutorny/MAC0350-Desenvolvimento-de-Sistemas-de-Software.git

Ou via https: git clone https://github.com/MikeFutorny/MAC0350-Desenvolvimento-de-Sistemas-de-Software.git

Depois entre na pasta do projeto:

cd projeto_pessoal

Antes de executar o backend é necessário instalar as dependências do projeto. Isso pode ser feito com:

pip install -r requirements.txt

Agora basta iniciar o servidor rodando:

uvicorn main:app --reload

A aplicação estará disponível em: http://127.0.0.1:8000

## Uso de Inteligência Artificial no Projeto

No desenvolvimento do Frontend a inteligência artificial foi utilizada de forma direta parar concepção do layout visual, gerando as estruturas de CSS e componentes responsivos. Além disso, a ferramenta foi fundamental na implementação da lógica do HTMX, ajudando a estruturar os atributos de troca de contexto e atualização parcial do DOM nos templates Jinja2. Os prompts descreviam o visual que eu esperava para o site e em geral o output batia com as sugestões, depois de alguns ajustes. Uma questão que a LLM usada (Gemini) não lidou bem foi box-sizing, sobre o qual li em https://www.w3schools.com/css/css3_box-sizing.asp.

No desenvolvimento do backend o uso de IA foi menos extenso, sendo usada para sugestões e para momentos específicos. 

A ferramenta auxiliou na ideia e implementação da Fórmula de Haversine para o cálculo geodésico de preços e na estruturação do Seed automático, gerando o conjunto de dados inicial das 30 cidades brasileiras. Também foram utilizadas sugestões de IA para o tratamento de strings vazias em filtros de busca e para a criação da rota de Reset, que facilitou o gerenciamento de cookies e testes de sessão em ambiente de desenvolvimento.

Implementação de Lazy Loading e Relacionamentos
A principal contribuição da IA no backend foi a orientação sobre o comportamento de Lazy Loading do SQLModel. Em sistemas relacionais, ao buscar uma Viagem, o banco de dados não traz automaticamente os objetos completos de Cidade (origem e destino). A IA sugeriu a técnica de forçar o carregamento desses objetos antes da renderização dos templates. Isso foi utilizado em múltiplos momentos ao longo do código.

Essa abordagem garantiu que a aplicação mantivesse uma alta performance nas consultas ao banco de dados, carregando dados relacionados apenas quando estritamente necessário para a interface do usuário.

A ferramenta também me sugeriu o uso de add_all, ao invés de adicionar em um loop como eu havia desenvolvido anteriormente.


## Autor

Mikhail Futorny

