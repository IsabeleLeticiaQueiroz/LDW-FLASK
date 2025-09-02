from flask import render_template,request, redirect, url_for
import urllib
# envia requisicoes a uma url
import json
#  faz a conversao de dados json p dicionario em python e vice e versa
def init_app(app):
    players = ['yan', 'ferrari', 'Valeria', 'Amanda']
    gamelist = [{'title': 'cs1.6', 'year': 1996, 'category': 'fps online'}]

    @app.route('/')
    def home():  # view function (FUNCAO DE VIZUALIZACAO)
        return render_template('index.html')
 
    @app.route('/games', methods=['GET', 'POST'])
    def games():  # view functio (FUNCAO DE VIZUALIZACAO)
        tittle = 'TaricIsland'
        year = 2002
        category = 'MMORPG'
        # dicionario em python
        console = {'Nome': 'playstation5',
                   'Fabricante': 'Sony', 'Ano': 2020}
        #tratando  uma requisicao POST em flask com request
        if request.method == 'POST':
            # COLETANDO O TEXT DO INPUT
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))
        return render_template('games.html', tittle=tittle, year=year, category=category, players=players, console=console)
    
    @app.route('/newgame', methods=['GET', 'POST'])
    def newGame():
        if request.method == 'POST':
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({
                    'title': request.form.get('title'),
                    'year': request.form.get('year'),
                    'category': request.form.get('category')
                })
                return redirect(url_for('newgame'))

        return render_template('newGame.html', gamelist=gamelist)
    @app.route('/apigames', methods=['GET', 'POST'])
    # criando parametro para rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url)
        data = response.read()
        gamesList = json.loads(data)
        if id:
            gameInfo = []
            for game in gamesList:
                if game['id'] == id:
                    gameInfo = game
                    break
            if gameInfo:
                return render_template('gameinfo.html', gameInfo=gameInfo)
            else:
                return f'Game com id {id} nao encontrado'
        else:
            return render_template('apigames.html', gamesList=gamesList)