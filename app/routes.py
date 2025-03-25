# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Review
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('home.html', reviews=reviews)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.bio = request.form.get('bio')
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('main.profile'))
    return render_template('profile.html')

@main.route('/about')
def about():
    return render_template('about.html')
