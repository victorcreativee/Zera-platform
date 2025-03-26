# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Review, Product
from . import db



main = Blueprint('main', __name__)

# Homepage
@main.route('/')
def home():
    trending_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()
    return render_template('home.html', reviews=trending_reviews)

# Profile Page
@main.route('/profile')
@login_required
def profile():
    # current_user is guaranteed to be valid because of @login_required
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', reviews=reviews)

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

# Optional: Add Review (if you're supporting registered users posting general reviews)
@main.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required.', 'danger')
            return redirect(url_for('main.add_review'))

        new_review = Review(title=title, content=content, author=current_user)
        db.session.add(new_review)
        db.session.commit()

        flash('Review added successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template('add_review.html')

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

# Product Detail + Submit Review (no login required)
@main.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("You must be logged in to submit a review.", "warning")
            return redirect(url_for('auth.login'))

        title = request.form.get('title')
        content = request.form.get('content')

        if not content:
            flash("Content is required.", "danger")
            return redirect(url_for('main.product_detail', product_id=product.id))

        review = Review(
            title=title,
            content=content,
            product_id=product.id,
            product=product,
            user_name=current_user.username,
            user_id=current_user.id
        )

        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully!', 'success')
        return redirect(url_for('main.product_detail', product_id=product.id))

    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
    return render_template('product_detail.html', product=product, reviews=reviews)