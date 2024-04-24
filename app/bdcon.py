from flask import Flask
import mysql.connector

dados = {
    "user":"lutheriafermino",
    "password":"teste",
    'host': '127.0.0.1',
    'database': 'lutheriafermino'
}

def mysq_con():
    conexao = mysql.connector.connect(**dados)
    return conexao

def conectado(conexao):
    if conexao.is_connected(){
        return 'Conectado'
    } else {
        return 'Desconectado'
    }

def mysql_close(conexao):
    conexao.close()
    return 'Conexão Fechada'