from app import db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin(app):
    with app.app_context():
        email = "admin@zera.com"
        password = "admin123"
        username = "victoradmin"

        existing_admin = User.query.filter_by(email=email).first()
        if not existing_admin:
            admin = User(
                username=username,
                email=email,
                is_admin=True
            )
            admin.set_password(password)  # Use method to set password
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin created successfully.")
        else:
            print("ℹ️ Admin already exists.")
