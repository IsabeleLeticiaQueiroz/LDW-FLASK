from flask import render_template
def init_app(app):
@app.route('/')
def home():
return render_template('index.html’)
@app.route('/games')
def games():
games = {'Título' : 'CS-GO', 'Ano' : 2012, 'Categoria' : 'FPS Online'}
jogadores = ['Pedro', 'João', 'Marcos', 'Maria']
return render_template('games.html', games=games, jogadores=jogadores)