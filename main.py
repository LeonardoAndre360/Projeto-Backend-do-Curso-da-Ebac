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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

meus_livrozinhos = {}

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

app.get("/")
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
def post_livros(id_livro: int, livro: Livro):
    if id_livro in meus_livrozinhos:
        raise HTTPException(status_code=400, detail="Este livro já existe!")
    else:
        meus_livrozinhos[id_livro] = livro.dict()
        return {"message": "O Livro foi criado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
def put_livros(id_livro: int, livro: Livro):
    meu_livro = meus_livrozinhos.get(id_livro)
    if not meu_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado!")
    else:
        meu_livro[id_livro] = livro.dict()

        return {"message": "As informações do seu livro foram autalizadas com sucesso!"}
    
@app.delete("/deletar/{id_livro}")
def delete_livros(id_livro: int):
    if id_livro not in meus_livrozinhos:
        raise HTTPException(status_code=404, detail="Esse livro não foi encontrado!")
    else:
        del meus_livrozinhos[id_livro]
        return {"message": "Seu livro foi deletado com sucesso!"}
