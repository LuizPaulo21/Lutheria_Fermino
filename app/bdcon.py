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

# Abre conexão
def mysql_con():
    conexao = mysql.connector.connect(**dados)

    return conexao

# Fecha conexão
def mysql_close(conexao):
    conexao.close()
    return 'Conexão Fechada'

# Consulta tabela de clientes por tipo de dado
def consulta_cliente(tipo, dado):

    tipo= str(tipo)
    dado = str(dado)

    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()
    query = f'SELECT * FROM cliente WHERE {tipo} = %s '
    cursor.execute(query, (dado,))

    resultado = cursor.fetchone()

    return resultado

# Consulta tabela de endereços
def consulta_endereco(idendereco):

    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM endereco WHERE idendereco = %s', (idendereco,))

    resultado = cursor.fetchone()

    return resultado

# Excluir Cliente
def excluir_cliente(tipo, dado):
    
    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()

    cursor.execute(f'SELECT * FROM cliente WHERE {tipo} = %s', (dado,))
    resultado = cursor.fetchone()

    if resultado:

        idcliente = resultado[0]
        idendereco = resultado[8]

        # Deleta da tabela cliente
        query = 'DELETE FROM cliente WHERE idcliente = %s'
        cursor.execute(query, (idcliente,))

        if cursor.rowcount > 0:

            # Deleta da tabela endereco
            query = 'DELETE FROM endereco WHERE idendereco = %s'
            cursor.execute(query, (idendereco,))

            conexao.commit()
            return "Excluido com sucesso!"
        
        else:
            return "Algo deu errado, por favor tente novamente!"
        
    else:
        return "Nenhum resultado encontrado!"