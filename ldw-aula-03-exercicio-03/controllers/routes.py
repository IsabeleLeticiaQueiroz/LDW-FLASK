from flask import Blueprint, render_template, request, redirect, url_for
import models.database as db

bp = Blueprint('routes', __name__)


@bp.route('/')
def index():
	return render_template('index.html')


@bp.route('/familias', methods=['GET', 'POST'])
def lista_familias():
	if request.method == 'POST':
		fid = request.form.get('id')
		payload = {
			'name': request.form.get('nome_familia'),
			'species': request.form.get('especie'),
			'members': request.form.get('membros'),
			'image': request.form.get('imagem', '')
		}
		if fid:
			try:
				db.update_family(int(fid), payload)
			except Exception:
				pass
		else:
			db.add_family(payload)
		return redirect(url_for('routes.lista_familias'))

	familias = db.get_families()
	edit_id = request.args.get('edit_id')
	edit_family = None
	if edit_id:
		try:
			edit_family = db.get_family(int(edit_id))
		except Exception:
			edit_family = None

	return render_template('lista_familias.html', familias=familias, edit_family=edit_family)


@bp.route('/familias/<int:fid>/delete', methods=['POST'])
def delete_familia(fid):
	db.delete_family(fid)
	return redirect(url_for('routes.lista_familias'))


@bp.route('/familias/<int:fid>/edit', methods=['GET'])
def edit_familia(fid):
	return redirect(url_for('routes.lista_familias', edit_id=fid))


@bp.route('/personagens', methods=['GET', 'POST'])
def tabela_personagens():
	if request.method == 'POST':
		cid = request.form.get('id')
		payload = {
			'name': request.form.get('nome'),
			'family': request.form.get('familia'),
			'age': request.form.get('idade'),
			'occupation': request.form.get('profissao'),
			'characteristic': request.form.get('caracteristica'),
			'image': request.form.get('imagem', '')
		}
		if cid:
			try:
				db.update_character(int(cid), payload)
			except Exception:
				pass
		else:
			db.add_character(payload)
		return redirect(url_for('routes.tabela_personagens'))

	personagens = db.get_characters()
	personagens_por_familia = {}
	for char in personagens:
		familia = char.get('family') or 'Sem Família'
		personagens_por_familia.setdefault(familia, []).append(char)

	edit_id = request.args.get('edit_id')
	edit_character = None
	if edit_id:
		try:
			edit_character = db.get_character(int(edit_id))
		except Exception:
			edit_character = None

	return render_template('tabela_personagens.html', personagens=personagens_por_familia, edit_character=edit_character)



@bp.route('/personagens/<int:cid>/delete', methods=['POST'])
def delete_personagem(cid):
	db.delete_character(cid)
	return redirect(url_for('routes.tabela_personagens'))


@bp.route('/personagens/<int:cid>/edit', methods=['GET'])
def edit_personagem(cid):
	return redirect(url_for('routes.tabela_personagens', edit_id=cid))


@bp.route('/galeria')
def galeria():
	familias = db.get_families()
	personagens = db.get_characters()
	personagens_por_familia = {}
	for char in personagens:
		familia = char.get('family') or 'Sem Família'
		personagens_por_familia.setdefault(familia, []).append(char)

	return render_template('galeria.html', familias=familias, personagens_por_familia=personagens_por_familia)


