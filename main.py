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
import redis
import json
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import asyncio

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

app = FastAPI(
    title="API de Livros.",
    description="API para gerenciar catálogos de livros.",
    version="1.0.0",
    contact={
        "name":"Leonardo André",
        "email":"Leonardoandre3600@gmail.com"
    }
)

MEU_USUARIO = os.getenv("MEU_USUARIO")
MINHA_SENHA = os.getenv("MINHA_SENHA")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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

def salvar_livro_redis(livro_id: int, livro: Livro):
    redis_client.set(f"livro:{livro_id}", json.dumps(livro.model_dump()))

def deletar_livro_redis(livro_id: int):
    redis_client.delete(f"livro:{livro_id}")

def sessao_db():
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
    return {"Hello": "World"}

@app.get("/debug/redis")
def ver_livro_redis():
    chaves = redis_client.keys("livros:*")
    livros = []

    for chave in chaves:
        valor = redis_client.get(chave)
        ttl = redis_client.ttl(chave)

        livros.append({"chave": chave, "valor": json.loads(valor), "ttl": ttl})

    return livros

@app.get("/livros")
def get_livros(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(sessao_db),
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores inválidos.")

    cache_key = f"livros:page{page}&limit{limit}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    livros = db.query(LivroDB).offset((page - 1) * limit).limit(limit).all()

    if not livros:
        return {"message": "Não existe livro nenhum!!"}

    total_livros = db.query(LivroDB).count()

    resposta = {
        "page": page,
        "limit": limit,
        "total": total_livros,
        "Livros": [
            {
                "id": livro.id,
                "nome_livro": livro.nome_livro,
                "autor_livro": livro.autor_livro,
                "ano_livro": livro.ano_livro
            } for livro in livros
        ]
    }

    redis_client.setex(cache_key, 30, json.dumps(resposta))

    return resposta

# id do livro
# nome do livro    
# autor do  livro
# ano de lançamento do livro

@app.post("/adiciona")
async def post_livros(livro: Livro, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.nome_livro == livro.nome_livro, LivroDB.autor_livro == livro.autor_livro).first()
    if db_livro:
        raise HTTPException(status_code=400, detail="Este livro já existe dentro do banco de dados!!!")
    
    novo_livro = LivroDB(nome_livro=livro.nome_livro, autor_livro=livro.autor_livro, ano_livro=livro.ano_livro)
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)

    salvar_livro_redis(novo_livro.id, livro)

    return {"message": "O livro foi adicionado com sucesso!"}
    
@app.put("/atualiza/{id_livro}")
async def put_livros(id_livro: int, livro: Livro,  db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()
    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado em seu banco de dados!")
    
    db_livro.nome_livro = livro.nome_livro
    db_livro.autor_livro = livro.autor_livro
    db_livro.ano_livro = livro.ano_livro
    
    db.commit()
    db.refresh(db_livro)
    
@app.delete("/deletar/{id_livro}")
async def delete_livros(id_livro: int, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_livro = db.query(LivroDB).filter(LivroDB.id == id_livro).first()

    if not db_livro:
        raise HTTPException(status_code=404, detail="Este livro não foi encontrado em seu banco de dados!!!")
    
    db.delete(db_livro)
    db.commit()

    deletar_livro_redis(id_livro)

    return {"message": "Seu livro foi deletado com sucesso!"}