#importando o flask, o nome do pacote é em minusculo
from flask import Flask, render_template 
from controllers import routes
from models.database import db
# importando biblioteca para manipular diretorios
import os
# criando instancia do flask
app = Flask(__name__, template_folder='views') #__name__ representa o nome da aplicacao
routes.init_app(app)
dir = os.path.abspath(os.path.dirname(__file__)) #pegando o diretorio atual do arquivo app.py
# CRIANDO ARQUIVO DO BANCO DE DADOS
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')  #configurando o banco de dados

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()  # criar o banco de dados se nao existir
    app.run(host='0.0.0.0', port=5000, debug=True)  # iniciar o servidor

# como rodar a aplicacao? "python app.py" no terminal
# a porta padrao do flask é 5000


