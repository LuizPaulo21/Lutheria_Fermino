from flask import Flask
from flaskext.mysql import MySQL


def iniciar_mysql(app):
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'seu_usuario'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'sua_senha'
    app.config['MYSQL_DATABASE_DB'] = 'lutheriafermino'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # Altere se o servidor MySQL estiver em outro local
    mysql.init_app(app)
    return mysql