from flask import Blueprint, render_template, request, redirect, url_for, session
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
        image_url = request.form.get('image_url')

        product = Product(
            title=title,
            description=description,
            image_url=image_url,
            company_id=company_id
        )

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
        db.session.commit()
        return redirect(url_for('company.company_dashboard'))

    return render_template('edit_product.html', product=product)

@company_bp.route('/company/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('auth.login_company'))

    product = Product.query.get_or_404(product_id)

    if product.company_id != company_id:
        return "Unauthorized", 403

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('company.company_dashboard'))
