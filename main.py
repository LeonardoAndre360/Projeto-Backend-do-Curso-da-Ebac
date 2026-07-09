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

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./livros.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

class LivroDB(Base):
    __tablename__ = "Livros"
    id = Column(Integer, primary_key=True, index=True)
    nome_livro = Column(String, index=True)
    autor_livro = Column(String, index=True)
    ano_livro = Column(Integer)

class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int

Base.metadata.create_all(bind=engine)


def sessão_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def get_livros(page: int = 10, limit: int = 10, db: Session = Depends(sessão_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores invalidos!!")
    
    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()

    if not livros:
        return{"message": "Não existe nenhum livro!!"}

    #livros_paginados = [
    #   {"id": id_livro, "nome_livro": livro_data["nome_data"], "autor_livro": livro_data["autor_livro"], "ano_livro": livro_data["ano_livro"]}
    #    for id_livro, livro_data in livros_ordenados[start:end]
    #]

    total_livros = db.query(LivroDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": total_livros,
        "livros": [{"id": livro.id, "nome_livro": livro.nome_livro, "autor_livro": livro.autor_livro, "ano_livro": livro.ano_livro} for livro in livros]
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
