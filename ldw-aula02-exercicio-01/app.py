from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URLs das suas APIs públicas
FAMILIES_API = "https://68c853475d8d9f5147350c80.mockapi.io/api/sylvanian-families/families"
CHARACTERS_API = "https://68c853475d8d9f5147350c80.mockapi.io/api/sylvanian-families/characters"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/familias', methods=['GET', 'POST'])
def lista_familias():
    if request.method == 'POST':
        nova_familia = {
            'name': request.form['nome_familia'],
            'species': request.form['especie'],
            'members': request.form['membros'],
            'image': request.form.get('imagem', '')
        }
        requests.post(FAMILIES_API, json=nova_familia)
        return redirect(url_for('lista_familias'))
    
    response = requests.get(FAMILIES_API)
    familias = response.json()
    return render_template('lista_familias.html', familias=familias)

@app.route('/personagens', methods=['GET', 'POST'])
def tabela_personagens():
    if request.method == 'POST':
        novo_personagem = {
            'name': request.form['nome'],
            'family': request.form['familia'],
            'age': request.form['idade'],
            'occupation': request.form['profissao'],
            'characteristic': request.form['caracteristica'],
            'image': request.form.get('imagem', '')
        }
        requests.post(CHARACTERS_API, json=novo_personagem)
        return redirect(url_for('tabela_personagens'))
    
    response = requests.get(CHARACTERS_API)
    characters = response.json()
    
    personagens_organizados = {}
    for char in characters:
        familia = char['family']
        if familia not in personagens_organizados:
            personagens_organizados[familia] = []
        personagens_organizados[familia].append(char)
    
    return render_template('tabela_personagens.html', personagens=personagens_organizados)

@app.route('/galeria')
def galeria():
    try:
        # Busca famílias da API
        response_familias = requests.get(FAMILIES_API)
        familias = response_familias.json()
        
        # Busca personagens da API
        response_personagens = requests.get(CHARACTERS_API)
        todos_personagens = response_personagens.json()
        
        # Organiza personagens por família
        personagens_por_familia = {}
        for char in todos_personagens:
            familia = char['family']
            if familia not in personagens_por_familia:
                personagens_por_familia[familia] = []
            personagens_por_familia[familia].append(char)
        
        return render_template('galeria.html', 
                             familias=familias, 
                             personagens_por_familia=personagens_por_familia)
    
    except Exception as e:
        print(f"Erro na galeria: {str(e)}")
        # Fallback: retorna template vazio se API falhar
        return render_template('galeria.html', 
                             familias=[], 
                             personagens_por_familia={})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)