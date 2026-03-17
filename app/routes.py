# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Car, Customer, User, Sale
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from functools import wraps

main_bp = Blueprint('main', __name__)

# Health check route
@main_bp.route('/health')
def health():
    return '<h1>✅ Flask is running!</h1><p>Application is working correctly.</p>'

def get_paginated_items(query, page=1, per_page=10):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    cars = Car.query.limit(3).all()
    return render_template('index.html', cars=cars)

@main_bp.route('/about')
def about():
    cars = Car.query.limit(5).all()
    return render_template('about.html', cars=cars)

@main_bp.route('/contacts')
def contacts():
    customers = Customer.query.limit(6).all()
    return render_template('contacts.html', customers=customers)

@main_bp.route('/cars')
def cars():
    page = request.args.get('page', 1, type=int)
    cars, pagination = get_paginated_items(Car.query, page, 10)
    return render_template('cars.html', cars=cars, pagination=pagination)

@main_bp.route('/sales')
def sales():
    page = request.args.get('page', 1, type=int)
    sales, pagination = get_paginated_items(Sale.query, page, 10)
    return render_template('sales.html', sales=sales, pagination=pagination)