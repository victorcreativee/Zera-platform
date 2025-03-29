# app/models.py

from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # ✅ Changed from `password` to `password_hash`
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bio = db.Column(db.Text, nullable=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)
    # total_points = db.Column(db.Integer, default=0)


    # ✅ Password setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # ✅ Password checker
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

    user_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    rating = db.Column(db.Integer, nullable=True)  # 1 to 5, rated by company
    points_awarded = db.Column(db.Integer, default=0)  # Points calculated from rating

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    status = db.Column(db.String(20), default='pending')  # 'pending' or 'approved'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='company', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    cover_image = db.Column(db.String(255), nullable=True)
    extra_images = db.Column(db.Text, nullable=True)

    company = db.relationship('Company', backref=db.backref('products', lazy=True))

    product_type = db.Column(db.String(50), default='Physical', nullable=False)  # 'Physical' or 'Digital'
    demo_link = db.Column(db.String(255), nullable=True)  # URL for demo, only relevant for digital products

class ProductForm(FlaskForm):
    title = StringField('Product Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    product_type = SelectField('Product Type', choices=[('Physical', 'Physical'), ('Digital', 'Digital')], default='Physical')
    demo_link = StringField('Demo Link (for Digital Products)', validators=[Length(max=255)])
    submit = SubmitField('Add Product')