from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import session


db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')  # Ensure this is added
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False

    db.init_app(app)
    Migrate(app, db)

    # Import Blueprints
    from .auth import auth
    from .routes import main

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
