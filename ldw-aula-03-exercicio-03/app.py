from flask import Flask

app = Flask(__name__, template_folder='views')

from controllers import routes  

try:
    app.register_blueprint(routes.bp)
except Exception:
    pass
import os
if os.environ.get('USE_DB'):
    try:
        from repositories.db import init_db as repo_init_db, db
        repo_init_db(app)
        with app.app_context():
            db.create_all()
    except Exception:
        from models.database import init_db as simple_init_db
        simple_init_db(app)
else:
    try:
        from models.database import init_db as simple_init_db
        simple_init_db(app)
    except Exception:
        pass
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=4000, debug=True)
