import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MysqlError

from database import executar_sql


app = FastAPI(title="FAST API 2INFO2")

@app.exception_handler(MysqlError)
def erro_de_banco(request: Request, exc: MysqlError):
    logging.getLogger("uvicorn.error").error("Erro de banco de dados: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro de banco de dados."},
    )

def representar_produto(produto):
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "quantidade": produto["quantidade"],
        "preco": format(produto["preco"], ".2f"),
    }

@app.get("/produtos")
def listar_produtos():
    sql = "SELECT * FROM produtos"
    produtos = executar_sql(sql)
    return {"produtos": [representar_produto(produto) for produto in produtos], "sintaxesql": {"sql": sql, "parametros": []}}
