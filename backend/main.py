
# Importa as classes principais do FastApi
from fastapi import FastAPI
# Importa o Middleware de CORs para permitir requisições de outros dominios(react)
from fastapi.middleware.cors import CORSMiddleware
# Import a classe do Pydantic para validação e estruturação de dados
from pydantic import BaseModel
# importa utilitários de tipagem do python 
from typing import Optional,List

# inicializa a aplicação do FastApi definindo o titulo e a versão da api
app = FastAPI(title="Api de Clientes", version="1.0")

# Adiciona o middleware de CORS na aplicação para evitar bloqueios de segunrança
# no navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Define o modelo de dados para criação de um cliente usando pydantic
# valida o que chega do frontend
class ClienteCreate(BaseModel):
    nome:str
    email:str
    telefone:Optional[str]=""
    empresa: Optional[str]=""
# Define o modelo completo do cliente herdando  de clientes 
# adicionando campos 

class Cliente(ClienteCreate):
    id:int
    active: bool =True

# Simula um banco de dados utilizando a lista dos clientes
clients_db:List[Cliente]=[
    Cliente(id=1,nome="Huguinho",email="huguinho@email.com",telefone="(11)12545-5555",empresa="Tech Solitions", active=True),
    Cliente(id=2,nome="Zezinho",email="zezinho@email.com",telefone="(21)5422-5855",empresa="Raiz Copy", active=True),
]
# Define a rota HTTP get para o endpoint que retorna a lista 
@app.get("/api/clients",response_model=List[Cliente])
def buscar_clientes():
    return clients_db

# Define a rota HTTP post para o endpoint que  cria o novo cliente
@app.post("/api/clients",response_model=Cliente, status_code=201)
def adicionar_clientes(client:ClienteCreate):
    novo_id = len(clients_db)+ 1
    novo_cliente = Cliente(
        id=novo_id,
        nome= client.nome,
        email = client.email,
        telefone = client.telefone,
        empresa = client.empresa,
        active=True
    )
    # adiciona o novo cliente à lista
    clients_db.append(novo_cliente)
    # returna o objeto do cliente criado
    return novo_cliente

