# app/auth.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Company
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/choose_role', methods=['GET', 'POST'])
def choose_role():
    # This route will display a form to choose whether the user is a company or an individual.
    return render_template('choose_role.html')



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Try logging in.', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Both fields are required!', 'error')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email not found. Please register first.', 'error')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password_hash, password):
            flash('Incorrect password. Please try again.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@auth.route('/register_company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        description = request.form.get('description')

        existing = Company.query.filter_by(email=email).first()
        if existing:
            flash('Email already registered. Please log in.')
            return redirect(url_for('auth.login_company'))

        company = Company(name=name, email=email, description=description)
        company.set_password(password)

        db.session.add(company)
        db.session.commit()

        flash('Company registered successfully! Please log in.')
        return redirect(url_for('auth.login_company'))

    return render_template('auth/register_company.html')


@auth.route('/login_company', methods=['GET', 'POST'])
def login_company():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        company = Company.query.filter_by(email=email).first()

        if not company or not company.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login_company'))

        if company.status != 'approved':
            flash('⏳ Your registration is still pending approval by the admin.', 'warning')
            return redirect(url_for('auth.login_company'))

        session['company_id'] = company.id
        session['company_name'] = company.name
        flash('✅ Logged in successfully.', 'success')
        return redirect(url_for('company.company_dashboard'))

    return render_template('auth/login_company.html')

@auth.route('/logout_company')
def logout_company():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('main.landing'))
