from app import app
from flask import request, session
from flask import render_template
from .bdcon import *
import hashlib
import dotenv
import os

#app.config.from_pyfile('config.py')
app.config['ALTO_CONTRASTE'] = False


dotenv.load_dotenv()
app.secret_key=os.getenv('SECRET_KEY')
cnx = mysql_con()
cursor = mysql_con().cursor()


@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html', ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Criação de login e sessão
@app.route("/login", methods=['POST'])
def check_login():
    # Checa se o método é POST e se os campos usuario e senha estão preenchidos
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Salva os dados do formulário nas variáveis
        usuario = request.form.get('username')
        senha = request.form.get('password')

        # Faz o hash da senha para evitar que a senha original seja exposta
        hash = senha + os.getenv('SECRET_KEY')
        hash = hashlib.sha1(hash.encode())
        senha = hash.hexdigest()

        # Checa se a conta existe no banco de dados
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM usuario WHERE usuario = %s AND senha = %s', (usuario, senha,))

        # Busca um registro e retorna o resultado
        usuario = cursor.fetchone()

        # Verificando se existe o usuario no banco de dados
        if usuario:
            # Dados da sessão
            session['loggedin'] = True
            session['id']= usuario[0]
            session['username']=usuario[1]

            # Redireciona ao inicio do sistema
            return render_template("base.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
        else:
            msg = "Usuario ou senha incorretos!"

    return render_template('index.html', msg=msg, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    
#Tela de cadastro de novos clientes
@app.route("/cadastrar.html")
def cadastrar():
    if session['loggedin'] == True:
        return render_template("cadastrar.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    else:
        return render_template("index.html", msg="Acesso negado, faça o login!", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Salva novo cliente no banco de dados    
@app.route("/salvar", methods=['POST'])
def salvar_cliente():
    if session['loggedin'] == True:

        # Busca os dados do formulario e salva nas variáveis
        cpf  = request.form.get('cpf')
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        complemento = request.form.get('complemento')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        cep = request.form.get('cep')
        telefone = request.form.get('telefone')
        celular = request.form.get('celular')
        contato = request.form.get('contato')
        email = request.form.get('email')
        observacao = request.form.get('observacao')

        #criação cursor
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM cliente WHERE CPF = %s', (cpf,))     

        # Busca um registro
        registro = cursor.fetchone()   

        # Se o registro existe
        if registro:
            return render_template('cadastrar.html', msg="Cliente já cadastrado", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE']) 
        else:
            #Insere primeiramente um enderço
            cursor.execute('INSERT INTO endereco (cep, logradouro, bairro, cidade, estado, complemento) VALUES (%s, %s, %s, %s, %s, %s)', (cep, endereco, bairro, cidade, estado, complemento))
            
            #retorna o id do ultimo registro da tabela
            ultimoid = cursor.lastrowid

            #insere finalmente o cliente
            cursor.execute('INSERT INTO cliente (CPF, nome, email, telefone, contato, celular, observacao, idendereco) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (cpf, nome, email, telefone, contato, celular, observacao, ultimoid))

            # Insere as informações no banco de dados
            cnx.commit()

            # Retorna mensagem de sucesso no cadastro
            return render_template("cadastrar.html", msg="Cliente cadastrado com sucesso!", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Página para busca de cadastro de cliente
@app.route("/buscar.html")
def buscar():
    if session['loggedin'] == True:
        return render_template("buscar.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    else:
        return render_template("index.html", msg="Acesso negado, faça o login!", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    
# Busca um registro de cliente no banco de dados
@app.route("/procurar", methods=['POST'])
def procurar():

    # Se usuario estiver logado
    if session['loggedin'] == True:

        # Salva os dados do formulário
        tipo = request.form.get('tipo')
        dado = request.form.get('textobusca')

        # Busca um registro
        resultado = consulta_cliente(tipo, dado)

        #Se o registro existe
        if resultado != None:
            endereco = consulta_endereco(resultado[8])

            return render_template("consultarres.html", dados = resultado, endereco = endereco, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
        else:
            return render_template("buscar.html", msg="Registro não existe na base de dados", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

 
# Página para inserir um pedido
@app.route("/pedido.html")
def incluir_pedido():
    
    marca = listar_marcas()

    return render_template("pedido.html", marcas = marca, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Função para gravar um pedido
@app.route("/salvar_pedido")
def salvar_pedido():

    dados_pedido = {
        # Buscar dados do formulário
        "cliente" : request.form.get("cliente"),
        "tipo" : request.form.get("Troca"),
        "prazo" : request.form.get("datetime"),
        "fabricante" : request.form.get("fabricante"),
        "peca" : request.form.get("peca"),
        "quantidade" : request.form.get("quantidade"),
        "valor" : request.form.get("valor"),
        "obs" : request.form.get("observacoes") }

    print(dados_pedido)


# Página para consultar um pedido
@app.route("/consultarpedido.html")
def consultar_pedido():
    return render_template("consultarpedido.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Página para cadastrar um pedido
@app.route("/cadastrarpedido.html")
def cadastrar_pedido():

    ultimoid = consultarultimoid()
    return render_template("cadastrarpedido.html", ultimoid = ultimoid, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Página para excluir um cliente
@app.route("/excluir.html")
def excluir():
    return render_template("excluir.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])


# Função para excluir um cliente
@app.route("/excluir", methods=['POST'])
def excluir_registro_cliente():

        # Se usuario estiver logado
    if session['loggedin'] == True:

        # Salva os dados do formulário
        tipo = request.form.get('tipo')
        dado = request.form.get('textobusca')

        # Exclui o cliente
        resultado = excluir_cliente(tipo, dado)

        return render_template("excluir.html", msg=resultado, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
        
    else:
        return render_template("index.html", msg="Faça Login!", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    

# Página para buscar um produto
@app.route("/buscarproduto.html")
def busca_item():

    return render_template("buscarproduto.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Função para buscar produtos
@app.route("/buscar_produtos", methods=['POST'])
def procura_produtos():
    
    #Salva os dados do formulário
    tipo = request.form.get('tipo')
    dado = request.form.get('textobusca')
    
    #Busca os dados no banco
    resultado = buscar_produtos(tipo, dado)

    if resultado:
        return render_template("listagemprodutos.html", resultado=resultado, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    else:
        return render_template("buscarproduto.html", msg="Nada encontrado! Por favor tente novamente.", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    
# Página para incluir um produto
@app.route("/incluirproduto.html")
def incluirproduto():

    listamarcas = listar_marcas()

    return render_template("incluirproduto.html", listamarcas=listamarcas, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])

# Função para Salvar Produto
@app.route("/salvarproduto", methods=['POST'])
def salvar_produto():

    nome = request.form.get('produto')
    marca = request.form.get('marca')

    resultado = salvarproduto(nome, marca)

    if resultado:
        retorno = listar_marcas()
        return render_template("incluirproduto.html", msg="Produto salvo com sucesso!", listamarcas = retorno, ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    else:
        return render_template("incluirproduto.html", msg="Algo deu errado, por favor tente novamente!", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
    

#Ativa/Desativa o alto contraste
@app.route("/altocontraste") 
def altocontraste():
    app.config['ALTO_CONTRASTE'] = not app.config['ALTO_CONTRASTE']
    return render_template("base.html", ALTO_CONTRASTE = app.config['ALTO_CONTRASTE'])
