from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'),
        static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
    )

    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)



    # Initialize Flask-Migrate
    migrate = Migrate(app, db)


    from .company import company_bp
    app.register_blueprint(company_bp)

    # Register blueprints
    with app.app_context():
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint)

        from .routes import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # from .company import company_bp
        # app.register_blueprint(company_bp)
        # from .admin_seed import create_admin
        # create_admin(app)
        
        from . import models


    return app

