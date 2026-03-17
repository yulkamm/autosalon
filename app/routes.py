# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Car, Customer, User, Sale
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from functools import wraps
import os

main_bp = Blueprint('main', __name__)

def get_paginated_items(query, page=1, per_page=10):
    """Пагинация записей"""
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Доступ запрещен. Только для администраторов.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# === ПУБЛИЧНЫЕ МАРШРУТЫ (ТОЛЬКО ПРОСМОТР) ===

@main_bp.route('/')
def index():
    """Главная страница - 3 автомобиля"""
    cars = Car.query.limit(3).all()
    return render_template('index.html', cars=cars)

@main_bp.route('/about')
def about():
    """Страница О нас - 5 автомобилей"""
    cars = Car.query.limit(5).all()
    return render_template('about.html', cars=cars)

@main_bp.route('/contacts')
def contacts():
    """Страница Контакты - 6 менеджеров"""
    customers = Customer.query.limit(6).all()
    return render_template('contacts.html', customers=customers)

@main_bp.route('/cars')
def cars():
    """Публичный каталог автомобилей с пагинацией"""
    page = request.args.get('page', 1, type=int)
    cars, pagination = get_paginated_items(Car.query, page, 10)
    return render_template('cars.html', cars=cars, pagination=pagination)

@main_bp.route('/sales')
def sales():
    """Публичный каталог продаж с пагинацией"""
    page = request.args.get('page', 1, type=int)
    sales, pagination = get_paginated_items(Sale.query, page, 10)
    return render_template('sales.html', sales=sales, pagination=pagination)

# === АВТОРИЗАЦИЯ ===

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход в систему"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Добро пожаловать, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже занято', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email уже зарегистрирован', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/logout')
@login_required
def logout():
    """Выход из системы"""
    logout_user()
    flash('Вы вышли из системы', 'success')
    return redirect(url_for('main.index'))

# === АДМИН ПАНЕЛЬ ===

@main_bp.route('/admin')
@login_required
def admin_dashboard():
    """Главная страница админ-панели"""
    if not current_user.is_admin:
        flash('Доступ запрещен. Только для администраторов.', 'error')
        return redirect(url_for('main.index'))
    
    cars_count = Car.query.count()
    sales_count = Sale.query.count()
    return render_template('admin/dashboard.html', cars_count=cars_count, sales_count=sales_count)

@main_bp.route('/admin/cars')
@login_required
def admin_cars():
    """Админ-панель: список автомобилей"""
    if not current_user.is_admin:
        flash('Доступ запрещен.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    cars, pagination = get_paginated_items(Car.query, page, 10)
    return render_template('admin/cars.html', cars=cars, pagination=pagination)

@main_bp.route('/admin/sales')
@login_required
def admin_sales():
    """Админ-панель: список продаж"""
    if not current_user.is_admin:
        flash('Доступ запрещен.', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    sales, pagination = get_paginated_items(Sale.query, page, 10)
    return render_template('admin/sales.html', sales=sales, pagination=pagination)

# === CRUD: АВТОМОБИЛИ ===

@main_bp.route('/admin/cars/add', methods=['GET', 'POST'])
@admin_required
def admin_car_add():
    """Добавить новый автомобиль"""
    if request.method == 'POST':
        # Автоматический выбор фото (циклично 1-10)
        cars_count = Car.query.count()
        photo_num = (cars_count % 10) + 1
        
        car = Car(
            brand=request.form.get('brand'),
            model=request.form.get('model'),
            year=int(request.form.get('year')),
            price=int(request.form.get('price')),
            color=request.form.get('color'),
            mileage=int(request.form.get('mileage')),
            engine=request.form.get('engine'),
            transmission=request.form.get('transmission'),
            photo=f'tables/cars/car_{photo_num}.jpg'
        )
        db.session.add(car)
        db.session.commit()
        
        flash(f'Автомобиль {car.brand} {car.model} успешно добавлен', 'success')
        return redirect(url_for('main.cars'))
    
    cars_count = Car.query.count()
    return render_template('admin/car_form.html', car=None, cars_count=cars_count)

@main_bp.route('/admin/cars/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_car_edit(id):
    """Редактировать автомобиль"""
    car = Car.query.get_or_404(id)
    
    if request.method == 'POST':
        car.brand = request.form.get('brand')
        car.model = request.form.get('model')
        car.year = int(request.form.get('year'))
        car.price = int(request.form.get('price'))
        car.color = request.form.get('color')
        car.mileage = int(request.form.get('mileage'))
        car.engine = request.form.get('engine')
        car.transmission = request.form.get('transmission')
        
        db.session.commit()
        
        flash(f'Автомобиль {car.brand} {car.model} успешно обновлен', 'success')
        return redirect(url_for('main.cars'))
    
    return render_template('admin/car_form.html', car=car)

@main_bp.route('/admin/cars/delete/<int:id>', methods=['POST'])
@admin_required
def admin_car_delete(id):
    """Удалить автомобиль"""
    car = Car.query.get_or_404(id)
    db.session.delete(car)
    db.session.commit()
    
    flash('Автомобиль успешно удален', 'success')
    return redirect(url_for('main.cars'))

# === CRUD: ПРОДАЖИ ===

@main_bp.route('/admin/sales/add', methods=['GET', 'POST'])
@admin_required
def admin_sale_add():
    """Добавить новую продажу"""
    if request.method == 'POST':
        # Автоматический выбор фото (циклично 1-10)
        sales_count = Sale.query.count()
        photo_num = (sales_count % 10) + 1
        
        sale = Sale(
            car_brand=request.form.get('car_brand'),
            car_model=request.form.get('car_model'),
            sale_date=datetime.strptime(request.form.get('sale_date'), '%Y-%m-%d').date(),
            sale_price=int(request.form.get('sale_price')),
            customer_name=request.form.get('customer_name'),
            customer_phone=request.form.get('customer_phone'),
            manager_name=request.form.get('manager_name'),
            payment_method=request.form.get('payment_method'),
            photo=f'tables/sales/sale_{photo_num}.jpg'
        )
        db.session.add(sale)
        db.session.commit()
        
        flash(f'Продажа {sale.car_brand} {sale.car_model} успешно добавлена', 'success')
        return redirect(url_for('main.sales'))
    
    return render_template('admin/sale_form.html', sale=None)

@main_bp.route('/admin/sales/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_sale_edit(id):
    """Редактировать продажу"""
    sale = Sale.query.get_or_404(id)
    
    if request.method == 'POST':
        sale.car_brand = request.form.get('car_brand')
        sale.car_model = request.form.get('car_model')
        sale.sale_date = datetime.strptime(request.form.get('sale_date'), '%Y-%m-%d').date()
        sale.sale_price = int(request.form.get('sale_price'))
        sale.customer_name = request.form.get('customer_name')
        sale.customer_phone = request.form.get('customer_phone')
        sale.manager_name = request.form.get('manager_name')
        sale.payment_method = request.form.get('payment_method')
        
        db.session.commit()
        
        flash('Продажа успешно обновлена', 'success')
        return redirect(url_for('main.sales'))
    
    return render_template('admin/sale_form.html', sale=sale)

@main_bp.route('/admin/sales/delete/<int:id>', methods=['POST'])
@admin_required
def admin_sale_delete(id):
    """Удалить продажу"""
    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()
    
    flash('Продажа успешно удалена', 'success')
    return redirect(url_for('main.sales'))

# === СТРАНИЦЫ ПРОСМОТРА ДЕТАЛЕЙ ===

@main_bp.route('/car/<int:id>')
def car_detail(id):
    """Просмотр деталей автомобиля"""
    car = Car.query.get_or_404(id)
    return render_template('car_detail.html', car=car)

@main_bp.route('/sale/<int:id>')
def sale_detail(id):
    """Просмотр деталей продажи"""
    sale = Sale.query.get_or_404(id)
    return render_template('sale_detail.html', sale=sale)