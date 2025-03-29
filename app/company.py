from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import db, Product, Company

company_bp = Blueprint('company', __name__)
print("✅ company_bp blueprint loaded")

@company_bp.route('/company/dashboard')
def company_dashboard():
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('auth.login_company'))

    company = Company.query.get(company_id)
    products = Product.query.filter_by(company_id=company_id).all()
    return render_template('company_dashboard.html', company=company, products=products)


@company_bp.route('/company/add_product', methods=['GET', 'POST'])
def add_product():
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('auth.login_company'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_url = request.form.get('image_url')  # original main image
        cover_image = request.form.get('cover_image')  # new cover image field
        extra_images = request.form.get('extra_images')  # optional extra image URLs (comma-separated)

        product = Product(
            title=title,
            description=description,
            image_url=image_url,
            cover_image=cover_image,
            company_id=company_id
        )

        # Optional: Save extra images if field exists in DB
        if hasattr(product, 'extra_images'):
            product.extra_images = extra_images

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('company.company_dashboard'))

    return render_template('add_product.html')

@company_bp.route('/company/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('auth.login_company'))

    product = Product.query.get_or_404(product_id)

    if product.company_id != company_id:
        return "Unauthorized", 403

    if request.method == 'POST':
        product.title = request.form.get('title')
        product.description = request.form.get('description')
        product.image_url = request.form.get('image_url')
        product.cover_image = request.form.get('cover_image')
        extra_images = request.form.get('extra_images')

        if hasattr(product, 'extra_images'):
            product.extra_images = extra_images

        db.session.commit()
        return redirect(url_for('company.company_dashboard'))

    return render_template('edit_product.html', product=product)

@company_bp.route('/company/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'success')
    return redirect(url_for('company.company_dashboard'))
 


