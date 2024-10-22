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
    
    
# Busca uma lista de produtos
def buscar_produtos(tipo, dado):
    
    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()

    #Define como a busca será feita
    if tipo == 'marca':
        #Busca id da marca
        query = 'SELECT idmarca FROM marca WHERE Marca = %s'
        cursor.execute(query, (dado,))
        id_marca = cursor.fetchone()

        if id_marca:
            # Busca produtos que possuem o idmarca encontrado
            query2 = 'SELECT * FROM produtos WHERE idmarca LIKE %s'
            resultado = cursor.execute(query2, (f"%{id_marca[0]}%",))
            resultado = cursor.fetchall()
            return resultado
        
        else:

            return None 
    else:
        # Busca pelo nome do produto
        query = 'SELECT * FROM produtos WHERE produto LIKE %s'
        resultado = cursor.execute(query, (f"%{dado}%",))
        resultado = cursor.fetchall()

        return resultado
    
# Função para listar todas as marcas cadastradas
def listar_marcas():
    
    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()

    query = 'SELECT * FROM marca'
    resultado = cursor.execute(query)
    resultado = cursor.fetchall()

    return resultado

# Função para salvar um novo produto
def salvarproduto(nome, marca):

    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()

    #Query para buscar id da marca
    query = "SELECT * FROM marca WHERE Marca = %s"
    cursor.execute(query, (marca,))
    idmarca = cursor.fetchone()

    # Query para inserção
    query2 = "INSERT INTO produtos (produto, idmarca) VALUES (%s, %s)"
    cursor.execute(query2, (nome, idmarca[0],))
    resultado = cursor.rowcount
    conexao.commit() # Confirmando a transação

    return resultado

#Consulta o ultimo id do pedido
def consultarultimoid():

    # Cria um cursor
    conexao = mysql_con()
    cursor = conexao.cursor()

    #query
    query = "SELECT LAST_INSERT_ID()"
    resultado = cursor.execute(query)
    
    if resultado == None:
        return 1
    else:
    
        return resultado