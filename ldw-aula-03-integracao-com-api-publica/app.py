#importando o flask, o nome do pacote é em minusculo
from flask import Flask, render_template 
from controllers import routes

# criando instancia do flask
app = Flask(__name__, template_folder='views') #__name__ representa o nome da aplicacao
routes.init_app(app)
# criando uma rota principal d aaplicacao


# @app.route('/')
# def home():#funcao que sera executada ao acessar a rota
#     return render_template('index.html') #puxa direto da views, nao precisa enderecar pasta

# @app.route('/games')
# def games():
#     title = 'the sims'
#     year =  '2014'
#     category = 'life simulator'
#     players = ['yan', 'ferrari', 'valeria', 'amanda']
#     console = {'nome': 'ps5', 'fabricante': 'sony', 'ano': 2020}
#     return render_template('games.html', 
#                            title = title,
#                            year = year,
#                            category = category, 
#                            players = players,
#                            console=console)


if __name__ == '__main__': #o servidor so roda se o name for igual a main (padrao)
    app.run(host='localhost', port=5000, debug=True) # iniciar o servidor


# como rodar a aplicacao? "python app.py" no terminal
# a porta padrao do flask é 5000


