from flask import Blueprint, render_template, request, redirect, url_for, flash

auth = Blueprint('auth', __name__) 


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email == "test@example.com" and password == "password":
            flash("Login successful!", "success")
            return redirect(url_for('main.homepage'))
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if username and email and password:
            flash("Registration successful!", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Please fill in all fields.", "error")

    return render_template('auth/register.html')
