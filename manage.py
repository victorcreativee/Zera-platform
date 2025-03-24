from app import create_app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

app = create_app()
migrate = Migrate(app, db)

# Use FlaskGroup to create migration commands
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
