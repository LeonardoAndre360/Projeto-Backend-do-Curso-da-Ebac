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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API de Livros.",
    description="API para gerenciar catálogos de livros.",
    version="1.0.0",
    contact={
        "name":"Leonardo André",
        "email":"Leonardoandre3600@gmail.com"
    }
)

meus_livrozinhos = []

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int
    lido: bool = False

@app.get("/")
def hello_world():
    return {"Hello": "Word"}

@app.get("/livros")
def get_livros():
    if not meus_livrozinhos:
        return {"message": "Não existe nenhum livro!"}
    else:
        return {"livros": meus_livrozinhos}
    
# id do livro
# nome do livro    
# autor do  livro
# ano de lançamento do livro

@app.post("/adiciona")
def post_livros(livro: Livro):
        meus_livrozinhos.append(livro)
        return {"message": "O Livro foi adicionado com sucesso!"}
    
@app.put("/atualiza/{nome_livro}")
def put_livros(nome_livro: str, livro_novo: Livro):
    for livro_atual in meus_livrozinhos:
        if livro_atual.nome_livro == nome_livro:
            posicao = meus_livrozinhos.index(livro_atual)
            meus_livrozinhos[posicao] = livro_novo
            return {"message": "O livro foi atualizado com sucesso"}
    raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")    
    
@app.delete("/deletar/{nome_livro}")
def delete_livros(nome_livro: str):
    for livro_atual in meus_livrozinhos:
        if livro_atual.nome_livro == nome_livro:
            meus_livrozinhos.remove(livro_atual)
            return {"message": "O livro foi deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
