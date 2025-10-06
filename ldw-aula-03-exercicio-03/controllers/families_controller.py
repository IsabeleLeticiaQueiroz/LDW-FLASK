from flask import Blueprint, render_template, request, redirect, url_for
import os

# choose repository depending on environment
if os.environ.get('USE_DB'):
    from repositories.sql_repo import get_all_families as get_families, create_family as post_family
else:
    from .api import get_families, post_family

bp = Blueprint('families', __name__)


@bp.route('/familias', methods=['GET', 'POST'])
def lista_familias():
    if request.method == 'POST':
        nova_familia = {
            'name': request.form.get('nome_familia'),
            'species': request.form.get('especie'),
            'members': request.form.get('membros'),
            'image': request.form.get('imagem', '')
        }
        post_family(nova_familia)
        return redirect(url_for('families.lista_familias'))
    familias_json = get_families()
    # API and DB return lists of dicts; templates accept dicts as well
    familias = familias_json
    return render_template('lista_familias.html', familias=familias)
