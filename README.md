# Sistema de Solicitação de Acessos

Aplicação desenvolvida em Django para gerenciamento de solicitações de acesso a sistemas internos.

A solução permite registrar solicitações, consultar seus dados, aprovar ou rejeitar solicitações e manter um histórico das decisões realizadas.

## Funcionalidades

- Criação de solicitações de acesso;
- Consulta de solicitações;
- Aprovação de solicitações;
- Rejeição de solicitações;
- Registro de justificativa para aprovação ou rejeição;
- Consulta do histórico de decisões;
- Prevenção de solicitações pendentes duplicadas;
- Validação das transições de status;
- Testes automatizados das principais regras de negócio;
- Execução utilizando Docker;
- PostgreSQL como banco de dados.

---

## Tecnologias

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose
- python-decouple

---

## Arquitetura

A aplicação foi organizada separando as responsabilidades das principais camadas:

```text
Cliente
   |
   v
API / Views
   |
   v
Serializers
   |
   v
Service Layer
   |
   v
Models / ORM
   |
   v
PostgreSQL
```

### Views

Responsáveis pela camada HTTP, recebendo as requisições e retornando as respostas.

### Serializers

Responsáveis pela serialização e validação dos dados utilizados pela API.

### Services

Concentram as regras de negócio relacionadas às decisões das solicitações, evitando que essas regras fiquem concentradas nas views.

### Models

Representam as entidades persistidas no banco de dados.

### DecisionHistory

Mantém o registro das decisões realizadas sobre as solicitações, permitindo rastreabilidade básica.

---

## Decisões arquiteturais

### Django

O Django foi utilizado como framework principal por fornecer recursos para desenvolvimento web, ORM, migrations, organização da aplicação e integração com banco de dados.

### Django REST Framework

O Django REST Framework foi utilizado para estruturar a camada de API.

A utilização de DRF foi uma decisão arquitetural e não uma exigência do enunciado. A escolha permite separar a camada HTTP da lógica de negócio e deixa a solução preparada para futuros consumidores, como uma interface web ou integrações com outros sistemas.

### Camada de serviço

As regras de aprovação e rejeição foram isoladas em uma camada de serviço para reduzir o acoplamento entre regras de negócio e camada HTTP.

### PostgreSQL

O PostgreSQL foi escolhido como banco de dados relacional para aproximar o ambiente de desenvolvimento de um cenário corporativo e evitar dependência do SQLite utilizado em uma configuração inicial do Django.

### Docker

Docker e Docker Compose foram utilizados para padronizar o ambiente de execução.

---

# Configuração do ambiente

## Pré-requisitos

Para executar o projeto utilizando Docker, é necessário ter instalado:

- Docker
- Docker Compose

Não é necessário instalar Python ou PostgreSQL diretamente na máquina quando a aplicação é executada pelo Docker.

---

# Execução com Docker

## 1. Clonar o projeto

```bash
git clone https://github.com/matheusmattesco/avaliacao_tecnica_python 
cd avaliacao_tecnica_python
```

## 2. Configurar o `.env`

Validar se o arquivo `.env` na raiz.

## 3. Construir e iniciar os containers

```bash
docker compose up --build
```

As migrations são executadas automaticamente na inicialização do container.

A aplicação será disponibilizada em:

```text
http://127.0.0.1:8000/
```

A API pode ser acessada em:

```text
http://127.0.0.1:8000/api/requests/
```

---

# API

## Listar solicitações

```http
GET /api/requests/
```

Retorna as solicitações cadastradas.

---

## Criar solicitação

```http
POST /api/requests/
```

Exemplo de payload:

```json
{
    "requester_name": "Matheus",
    "requester_email": "matheus@email.com",
    "system": "SAP",
    "profile": "Administrador",
    "justification": "Necessário para execução das atividades."
}
```

Uma nova solicitação é criada inicialmente com status:

```text
PENDENTE
```

---

## Aprovar solicitação

```http
POST /api/requests/{id}/approve/
```

Exemplo:

```json
{
    "decision_reason": "Acesso necessário para execução das atividades."
}
```

A justificativa da decisão é obrigatória.

---

## Rejeitar solicitação

```http
POST /api/requests/{id}/reject/
```

Exemplo:

```json
{
    "decision_reason": "O perfil solicitado não é necessário."
}
```

A justificativa da decisão é obrigatória.

---

## Consultar histórico

```http
GET /api/requests/{id}/history/
```

Retorna o histórico de decisões da solicitação.

O histórico registra, entre outras informações, a ação realizada e a justificativa fornecida.

---

# Regras de negócio

## Status inicial

Toda solicitação criada inicia como:

```text
PENDENTE
```

## Duplicidade

Não é permitida uma nova solicitação PENDENTE com a mesma combinação de:

- e-mail do solicitante;
- sistema;
- perfil.

## Aprovação e rejeição

Uma solicitação PENDENTE pode ser:

```text
PENDENTE -> APROVADO
```

ou:

```text
PENDENTE -> REJEITADO
```

Uma solicitação já decidida não pode receber uma nova decisão.

## Justificativa

A aprovação ou rejeição exige uma justificativa.

## Auditoria

Toda aprovação ou rejeição gera um registro em `DecisionHistory`.

---

# Testes automatizados

Os principais cenários e regras de negócio são cobertos por testes automatizados.

Atualmente são contemplados:

1. Criação de solicitação;
2. Impedimento de solicitação pendente duplicada;
3. Aprovação de solicitação pendente;
4. Rejeição de solicitação pendente;
5. Aprovação sem justificativa;
6. Rejeição sem justificativa;
7. Tentativa de aprovar solicitação já aprovada;
8. Tentativa de rejeitar solicitação já rejeitada;
9. Criação de histórico após aprovação;

## Executar os testes

Dentro do Docker:

```bash
docker compose exec web python manage.py test
```

Os testes do Django utilizam um banco de testes separado, evitando que os registros criados durante os testes sejam mantidos no banco de desenvolvimento.

---

# Banco de dados

O projeto utiliza PostgreSQL através do Docker Compose.

A estrutura básica é:

```text
Docker Compose
|
+-- web
|   +-- Django
|   +-- Django REST Framework
|
+-- db
    +-- PostgreSQL
```

O Django acessa o banco utilizando o hostname:

```env
DB_HOST=db
```
---