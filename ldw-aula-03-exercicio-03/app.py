from flask import Flask

# create app (templates are in 'views')
app = Flask(__name__, template_folder='views')

# register controllers through a single routes module (professor pattern)
from controllers import routes  # noqa: F401  (module provides the routes blueprint)

# register the blueprint exported by controllers.routes
try:
    app.register_blueprint(routes.bp)
except Exception:
    # if routes doesn't expose bp, ignore (backward compatibility)
    pass

# initialize DB if requested (development helper)
import os
# If USE_DB is set we may use the repository initializer; otherwise use the
# simpler professor-style sqlite initializer in models.database for parity.
if os.environ.get('USE_DB'):
    try:
        from repositories.db import init_db as repo_init_db, db
        repo_init_db(app)
        with app.app_context():
            db.create_all()
    except Exception:
        # fall back to simpler DB init
        from models.database import init_db as simple_init_db
        simple_init_db(app)
else:
    # professor-style sqlite initialization
    try:
        from models.database import init_db as simple_init_db
        simple_init_db(app)
    except Exception:
        pass
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)