from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional
import secrets

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "sqlite:///./tarefas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI(
    title="API de Tarefas.",
    description="API para gerenciar tarefas.",
    version="1.0.0",
    contact={
        "name":"Leonardo André",
        "email":"Leonardoandre3600@gmail.com"
    }
)

MEU_USUARIO = "admin"
MINHA_SENHA = "admin"

security = HTTPBasic()



class TarefaDB(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False)

class Tarefa(BaseModel):
    titulo: str
    descricao: str
    concluida: bool

Base.metadata.create_all(bind=engine)


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
    return {"Hello": "Word"}

@app.get("/tarefas")
def get_tarefas(page: int = 1, limit: int = 10, db: Session = Depends(sessao_db) , credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou limit estão com valores invalidos!!")
    
    tarefas = db.query(TarefaDB).offset((page - 1) * limit).limit(limit).all()

    if not tarefas:
        return{"message": "Não existe nenhuma tarefa!!"}

    total_tarefas = db.query(TarefaDB).count()

    return {
        "page": page,
        "limit": limit,
        "total": total_tarefas,
        "tarefas": [{"id": tarefa.id, "titulo": tarefa.titulo, "descricao": tarefa.descricao, "concluida": tarefa.concluida} for tarefa in tarefas]
    }


@app.post("/tarefas")
def post_tarefas(tarefa: Tarefa, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.titulo == tarefa.titulo, TarefaDB.descricao == tarefa.descricao).first()
    if db_tarefa:
        raise HTTPException(status_code=400, detail="Esta tarefa já existe dentro do banco de dados!!!")
    
    nova_tarefa = TarefaDB(titulo=tarefa.titulo, descricao=tarefa.descricao, concluida=tarefa.concluida)
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return {"message": "A tarefa foi adicionada com sucesso!"}
    
@app.put("/tarefas/{id_tarefa}")
def put_tarefas(id_tarefa: int, tarefa: Tarefa,  db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id_tarefa).first()
    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Esta tarefa não foi encontrada em seu banco de dados!")
    
    db_tarefa.titulo = tarefa.titulo
    db_tarefa.descricao = tarefa.descricao
    db_tarefa.concluida = tarefa.concluida
    
    db.commit()
    db.refresh(db_tarefa)

    return {"message": "A tarefa foi atualizada com sucesso!"}
    
@app.delete("/tarefas/{id_tarefa}")
def delete_tarefas(id_tarefa: int, db: Session = Depends(sessao_db) ,credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)):
    db_tarefa = db.query(TarefaDB).filter(TarefaDB.id == id_tarefa).first()

    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Esta tarefa não foi encontrada em seu banco de dados!!!")
    
    db.delete(db_tarefa)
    db.commit()

    return {"message": "Sua tarefa foi deletada com sucesso!"}
