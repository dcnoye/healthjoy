from datetime import datetime
import uuid
from flask import Flask




def create_app():
    """Create a Flask applicaction.
    """
    # Instantiate Flask
    app = Flask(__name__)
    app.secret_key = f'super secret key - {uuid.uuid4().hex[0:12]}'
    # Register blueprints
    from app.extensions.jinja import jinja_extensions_blueprint
    app.register_blueprint(jinja_extensions_blueprint)
    app.jinja_env.globals.update(now=datetime.utcnow)

    from app.views.home_views import home_blueprint
    app.register_blueprint(home_blueprint)

    return app
