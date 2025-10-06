from flask import Blueprint, render_template, request, redirect, url_for
import os

# choose repository depending on environment
if os.environ.get('USE_DB'):
    from repositories.sql_repo import get_all_characters as get_characters, create_character as post_character
else:
    from .api import get_characters, post_character

bp = Blueprint('characters', __name__)


@bp.route('/personagens', methods=['GET', 'POST'])
def tabela_personagens():
    if request.method == 'POST':
        novo_personagem = {
            'name': request.form.get('nome'),
            'family': request.form.get('familia'),
            'age': request.form.get('idade'),
            'occupation': request.form.get('profissao'),
            'characteristic': request.form.get('caracteristica'),
            'image': request.form.get('imagem', '')
        }
        post_character(novo_personagem)
        return redirect(url_for('characters.tabela_personagens'))

    characters_json = get_characters()
    personagens_organizados = {}
    for char in characters_json:
        familia = char.get('family')
        if familia not in personagens_organizados:
            personagens_organizados[familia] = []
        personagens_organizados[familia].append(char)

    return render_template('tabela_personagens.html', personagens=personagens_organizados)
