# Projeto Backend de Livros - FastAPI & Docker

Este repositório contém uma aplicação FastAPI conteinerizada utilizando Docker, Docker Compose e gerenciamento de dependências com Poetry. Este projeto foi desenvolvido como prática de infraestrutura e deployment de aplicações Python.

## Tecnologias Utilizadas
- **Python 3.14**
- **FastAPI**
- **Poetry** (Gerenciador de pacotes)
- **Docker & Docker Compose**
- **SQLite** (Banco de dados)

## Como rodar o projeto localmente

### Pré-requisitos
Certifique-se de ter o [Docker](https://www.docker.com/) e o [Docker Compose](https://docs.docker.com/compose/) (ou Podman) instalados na sua máquina.

### Passo a passo

1. **Clone o repositório:**
   Abra o seu terminal e rode o comando abaixo para baixar o código:
   git clone https://github.com/LeonardoAndre360/Projeto-Backend-do-Curso-da-Ebac.git

### 2. Configurações Necessárias (Variáveis de Ambiente)
Antes de subir a aplicação, é necessário configurar o banco de dados.
1. Na raiz do projeto, crie um arquivo chamado `.env`.
2. Adicione a seguinte linha dentro do arquivo:
`DATABASE_URL=sqlite:///./livros.db`

### 3. Build e Execução com Docker Compose
Para construir a imagem Docker e subir o container da aplicação em segundo plano, execute:
```bash
podman compose up --build -d