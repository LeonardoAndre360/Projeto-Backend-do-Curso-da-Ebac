# API de Livros

# GET, POST, PUT, DELETE

# POST - Adicionar novos Livros (Create)
# GET - Buscar os dados dos Livros (Read)
# PUT - Atualizar informações dos Livros (Update)
# DELETE - Deletar informações dos Livros (Delete)

# CRUD

# Create
# Read
# Update
# Delete

# Vamos acessar nosso ENDPOINT
# E vamos acessar os PATH's desse

# Path ou Rota
# Query Strings

# 200 300 400 500

# Fábrica -> Logista -> Consumidor 

# Documentação Swagger -> Documentar os endpoints da nossa aplicação (da nossa API)

# Olha, acessa minha documentação swagger nesse endpoint -> http://endpointdelivros/docs/

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets
import os

app = FastAPI(
    title="API de Livros.",
    description="API para gerenciar catálogos de livros.",
    version="1.0.0",
    contact={
        "name":"Leonardo André",
        "email":"Leonardoandre3600@gmail.com"
    }
)

MEU_USUARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()


meus_livrozinhos = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Basic"}
        )


@app.get("/")
def hello_world():
    return {"Hello": "Word"}

@app.get("/livros")
def get_livros(page: int = 1, size: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario), ordem: Optional[str] = "id"):
    campos_validos = ["id", "nome", "ano"]
    if ordem not in campos_validos:
        raise HTTPException(status_code=400, detail="Campo de ordenação inválido! Use id, nome ou ano.")
    if page < 1 or size < 1:
        raise HTTPException(status_code=400, detail="Page ou size estão com valores invalidos!!")
    
    if not meus_livrozinhos:
        return{"message": "Não existe nenhum livro!!"}
    
    if ordem == "nome":
        livros_ordenados = sorted(meus_livrozinhos.items(), key=lambda x: x[1]["nome_livro"])
    elif ordem == "ano":
        livros_ordenados = sorted(meus_livrozinhos.items(), key=lambda x: x[1]["ano_livro"])
    else:
        livros_ordenados = sorted(meus_livrozinhos.items(), key=lambda x: x[0])

    start = (page - 1) * size
    end = start + size

    livros_paginados = [
        {"id": id_livro, "nome_livro": livro_data["nome_livro"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
        for id_livro, livro_data in livros_ordenados[start:end]
    ]

    return {
        "page": page,
        "size": size,
        "total": len(meus_livrozinhos),
        "livros": livros_paginados
    }

# id do livro
# nome do livro    
# autor do  livro
# ano de lançamento do livro

@app.post("/adiciona")
def post_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Este livro já existe!")
    else:
        meus_livrozinhos[id_livro] = livro.model_dump()
        return {"message": "O Livro foi criado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
    else:
        # Eu jogo essa antiga informação dentro do meu antigo dicionário (que é o "meus_livrozinhos")
        # E não dentro da referência do antigo dicionário
        # Antigo dicionário != Referência do antigo dicionário
        meus_livrozinhos[id_livro] = livro.model_dump()
        return {"message": "As informações do seu livro foram autalizadas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livros(id_livro: int, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]
        return {"message": "Seu livro foi deletado com sucesso!"}
