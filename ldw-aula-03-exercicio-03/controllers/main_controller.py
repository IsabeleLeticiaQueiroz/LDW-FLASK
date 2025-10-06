from flask import Blueprint, render_template
from .api import get_families, get_characters

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/galeria')
def galeria():
    try:
        familias = get_families()
        todos_personagens = get_characters()

        personagens_por_familia = {}
        for char in todos_personagens:
            familia = char.get('family')
            if familia not in personagens_por_familia:
                personagens_por_familia[familia] = []
            personagens_por_familia[familia].append(char)

        return render_template('galeria.html', familias=familias, personagens_por_familia=personagens_por_familia)

    except Exception as e:
        print(f"Erro na galeria: {e}")
        return render_template('galeria.html', familias=[], personagens_por_familia={})
