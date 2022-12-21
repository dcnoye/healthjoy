from datetime import datetime
from flask import Flask




def create_app():
    """Create a Flask applicaction.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Register blueprints
    from app.extensions.jinja import jinja_extensions_blueprint
    app.register_blueprint(jinja_extensions_blueprint)
    app.jinja_env.globals.update(now=datetime.utcnow)

    from app.views.home_views import home_blueprint
    app.register_blueprint(home_blueprint)

    return app
