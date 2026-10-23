import os 
from pathlib import Path
import mysql.connector 
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

def executar_sql(sql, parametros=()):
    conexao = None
    cursor = None
    try:
        conexao = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"]
        )
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall() if cursor.with_rows else []
        conexao.commit()
        return resultados
    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None:
            conexao.close()
