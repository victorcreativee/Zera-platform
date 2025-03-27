# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user, login_user
from .models import Review, Product, Company, User
from werkzeug.security import check_password_hash
from . import db
from datetime import datetime



main = Blueprint('main', __name__)

# Homepage
@main.route('/home')
def home():
    trending_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()
    return render_template('home.html', reviews=trending_reviews)

# Landing Page
@main.route('/')
def landing():
    products = Product.query.all()
    products = sorted(products, key=lambda p: len(p.reviews), reverse=True)
    trending_products = products[:6]
    for p in trending_products:
        p.review_count = len(p.reviews)
    return render_template('landing.html', trending_products=trending_products)

# Profile Page
@main.route('/profile')
@login_required
def profile():
    # current_user is guaranteed to be valid because of @login_required
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    review_count = len(reviews)
    return render_template('profile.html', reviews=reviews, review_count=review_count)

# User Dashboard
@main.route('/dashboard')
@login_required
def user_dashboard():
    # For now, show all products (you'll filter later by access)
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('user_dashboard.html', products=products)

# About Page
@main.route('/about')
def about():
    return render_template('about.html')


# Edit Review
@main.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash("You are not authorized to edit this review.", "danger")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        review.title = request.form.get('title')
        review.content = request.form.get('content')
        db.session.commit()

        flash('Review updated successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('edit_review.html', review=review)

# Delete Review
@main.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)

    if review.user_id != current_user.id:
        flash("You are not authorized to delete this review.", "danger")
        return redirect(url_for('main.home'))

    db.session.delete(review)
    db.session.commit()

    flash('Review deleted successfully!', 'success')
    return redirect(url_for('main.home'))

# Public list of all products
@main.route('/products')
def all_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('public_products.html', products=products)

# Route to add a review
@main.route('/product/<int:product_id>/review', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_review = Review(
            title=title,
            content=content,
            product_id=product.id,
            user_id=current_user.id
        )

        db.session.add(new_review)
        db.session.commit()

        flash('Your review has been added!', 'success')
        return redirect(url_for('main.product_detail', product_id=product.id))

    return render_template('add_review.html', product=product)
    
# Route to view product details
@main.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Ensure user_name is taken from the authenticated user
        user_name = current_user.username if current_user.is_authenticated else 'Anonymous'

        review = Review(
            title=title,
            content=content,
            product_id=product.id,
            user_name=user_name,  # Set user_name here
            user_id=current_user.id if current_user.is_authenticated else None,
            created_at=datetime.now()
        )

        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully!', 'success')
        return redirect(url_for('main.product_detail', product_id=product.id))

    return render_template('product_detail.html', product=product, reviews=reviews)



@main.route('/product/<int:product_id>/reviews')
def product_reviews(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()  # Fetch reviews for the product
    return render_template('product_reviews.html', product=product, reviews=reviews)


@main.route('/admin/approve_company/<int:company_id>')
@login_required
def approve_company(company_id):
    if not current_user.is_admin:
        flash("Unauthorized", "danger")
        return redirect(url_for('main.home'))

    company = Company.query.get_or_404(company_id)
    company.status = 'approved'
    db.session.commit()
    flash(f"{company.name} approved!", "success")
    return redirect(url_for('main.admin_dashboard'))

@main.route('/company/signup', methods=['GET', 'POST'])
def company_signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        description = request.form.get('description')

        if not name or not email or not password:
            flash("Name, Email, and Password are required.", "danger")
            return redirect(url_for('main.company_signup'))

        existing = Company.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered.", "warning")
            return redirect(url_for('main.company_signup'))

        new_company = Company(
            name=name,
            email=email,
            description=description
        )
        new_company.set_password(password)
        db.session.add(new_company)
        db.session.commit()

        flash("Signup successful! Awaiting admin approval.", "success")
        return redirect(url_for('main.home'))

    return render_template('company_signup.html')

@main.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for('main.admin_login'))

        if not user.is_admin:
            flash("You are not authorized to access the admin dashboard.", "danger")
            return redirect(url_for('main.home'))

        login_user(user)
        return redirect(url_for('main.admin_dashboard'))

    return render_template('admin_login.html')

# Admin dashboard
@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.home'))

    companies = Company.query.order_by(Company.created_at.desc()).all()
    return render_template('admin_dashboard.html', companies=companies)

@main.route('/add-company', methods=['GET', 'POST'])
@login_required
def add_company():
    if not current_user.is_admin:
        flash("Unauthorized access", "danger")
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        description = request.form.get('description')

        # Basic validation
        if not name or not email or not password:
            flash("Name, Email, and Password are required.", "danger")
            return redirect(url_for('main.add_company'))

        # Check if the company already exists
        existing_company = Company.query.filter_by(email=email).first()
        if existing_company:
            flash("Company with this email already exists.", "warning")
            return redirect(url_for('main.add_company'))

        # Create the new company
        new_company = Company(
            name=name,
            email=email,
            description=description
        )
        new_company.set_password(password)  # Set password hash

        db.session.add(new_company)
        db.session.commit()

        flash(f"Company {name} added successfully! Awaiting admin approval.", "success")
        return redirect(url_for('main.admin_dashboard'))

    return render_template('add_company.html')