from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

familias = []
personagens = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/familias', methods=['GET', 'POST'])
def lista_familias():
    if request.method == 'POST':
        nome_familia = request.form['nome_familia']
        especie = request.form['especie']
        casa = request.form['casa']
        membros = request.form['membros']
        print("=== DADOS RECEBIDOS ===")
        print("Nome:", nome_familia)
        familias.append({
            'nome_familia': nome_familia,
            'especie': especie,
            'casa': casa,
            'membros': membros,
        })
        return redirect(url_for('lista_familias'))
    return render_template('lista_familias.html', familias=familias)

@app.route('/personagens', methods=['GET', 'POST'])
def tabela_personagens():
    if request.method == 'POST':
        nome = request.form['nome']
        familia = request.form['familia']
        idade = request.form['idade']
        profissao = request.form['profissao']
        caracteristica = request.form['caracteristica']
        if familia not in personagens:
            personagens[familia] = []
        personagens[familia].append({
            'nome': nome,
            'idade': idade,
            'profissao': profissao,
            'caracteristica': caracteristica,
        })
        return redirect(url_for('tabela_personagens'))
    return render_template('tabela_personagens.html', personagens=personagens)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)