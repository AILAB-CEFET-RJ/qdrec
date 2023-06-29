# Querido Diário

## Repositório para armazenamento de script de recomendação de trechos de diário oficial com base em uma determinada consulta

Saiba mais https://queridodiario.ok.org.br/

## Requisitos

- Docker
- Python 3.9+
- Pipenv

## API

Este projeto possui uma API feita em Python com FastAPI que se conecta à um banco de dados para armazenar metadados de entradas do Diário Oficial e dados processados em cima dessa entrada.

## Como executar

Para executar as dependências rode o comando `docker compose up` na raiz do projeto para disponibilizar a base de dados.
Após o banco de dados estar disponível, execute o comando `uvicorn main:app --reload` para iniciar o servidor da API.

## Rotas

Essa API possui as seguintes rotas:

### GET
`/excerpt_metadata/`
Retorna uma lista de metadados das entradas do Diário Oficial registradas no banco de dados.

`/excerpt_metadata/{excerpt_id}`
Retorna uma entrada metadados do Diário Oficial registrada no banco de dados com id = excerpt_id.

`/entities/`
Retorna uma lista de entidades encontradas nas entradas do Diário Oficial.

`/entities/{excerpt_id}`
Retorna uma lista de entidades encontradas na entrada do Diário Oficial com id = excerpt_id.

`/vectors/{excerpt_id}`
Retorna uma lista de vetores de recomendação encontrados na entrada do Diário Oficial com id = excerpt_id.

### POST
`/excerpt_metadata/`
Registra uma entrada de metadados de uma entrada do Diário Oficial no banco de dados recebendo um JSON:
``` 
{
    "excerpt_id": "123"
    "uf": "RJ"
    "cidade": "Rio de Janeiro"
    "tema": "Diário Oficial"
    "data": "2023-01-01"
}
```

`/entities/`
Registra uma entrada de entidade no banco de dados recebendo um JSON:
``` 
{
    "excerpt_id": "123"
    "content": "A"
    "entity_type": "PESSOA"
    "start_offset": 0
    "end_offset": 1
}
```