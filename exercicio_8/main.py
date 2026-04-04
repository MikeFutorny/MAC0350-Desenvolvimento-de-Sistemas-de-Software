from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/img", StaticFiles(directory="static/img"), name="img")

likes = 0


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()




@app.get("/curtidas", response_class=HTMLResponse)
def pagina_curtidas():
    with open("templates/curtidas.html") as f:
        return f.read()


@app.post("/curtir", response_class=HTMLResponse)
def curtir(acao: str = "somar"):
    global likes

    if acao == "reset":
        likes = 0
    else:
        likes += 1

    return f"""
    <section class="card" id="likes-container">
        <h2>Likes: {likes}</h2>

        <button hx-post="/curtir"
                hx-target="#likes-container"
                hx-swap="innerHTML">
            Like!
        </button>

        <button hx-post="/curtir?acao=reset"
                hx-target="#likes-container"
                hx-swap="innerHTML"
                hx-confirm="Are you sure you want to reset likes?">
            Reset
        </button>
    </section>
    """


@app.get("/professor/sobre", response_class=HTMLResponse)
def sobre():
    with open("templates/professor/sobre.html") as f:
        return f.read()


@app.get("/professor/ensino", response_class=HTMLResponse)
def ensino():
    with open("templates/professor/ensino.html") as f:
        return f.read()


@app.get("/professor/publicacoes", response_class=HTMLResponse)
def publicacoes():
    with open("templates/professor/publicacoes.html") as f:
        return f.read()


@app.get("/professor/contato", response_class=HTMLResponse)
def contato():
    with open("templates/professor/contato.html") as f:
        return f.read()
    
@app.get("/jupiter", response_class=HTMLResponse)
def jupiter():
    with open("templates/jupiter.html") as f:
        return f.read()