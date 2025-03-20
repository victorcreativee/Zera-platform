from flask import Flask
from .routes import main
from .auth import auth

def create_app():
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static') 
    # app = Flask(__name__, static_folder='../static')
    app.secret_key = 'supersecretkey'

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
