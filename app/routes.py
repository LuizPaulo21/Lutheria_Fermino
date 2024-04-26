from app import app
from flask import request, session
from flask import render_template
from .bdcon import *
import hashlib
import dotenv
import logging
import os



dotenv.load_dotenv()
app.secret_key=os.getenv('SECRET_KEY')

@app.route("/")
@app.route("/index")
def home():
    return render_template('index.html')


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
        cnx = mysql_con()
        cursor = cnx.cursor()
        cursor.execute('SELECT * FROM usuario WHERE usuario = %s AND senha = %s', (usuario, senha,))

        # Busca um registro e retorna o resultado
        usuario = cursor.fetchone()
        print(usuario)

        # Verificando se existe o usuario no banco de dados
        if usuario:
            # Dados da sessão
            session['loggedin'] = True
            session['id']= usuario[0]
            session['username']=usuario[1]

            # Redireciona ao inicio do sistema
            return render_template("base.html")
        else:
            msg = "Usuario ou senha incorretos!"

    return render_template('index.html', msg=msg)


    
#Tela de cadastro de novos clientes
@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastrar.html")