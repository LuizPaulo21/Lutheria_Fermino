from flask import Flask
import mysql.connector
import dotenv
import os


dotenv.load_dotenv()


dados = {
    "user": os.getenv('MYSQL_USERNAME'),
    "password": os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE')
}

def mysql_con():
    conexao = mysql.connector.connect(**dados)
    return conexao


def mysql_close(conexao):
    conexao.close()
    return 'Conexão Fechada'

