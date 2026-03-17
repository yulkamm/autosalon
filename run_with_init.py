import os
from app import create_app, db
from app.models import User, Car, Sale, Customer
from datetime import datetime, timedelta
import random

# Создаем приложение
app = create_app()

with app.app_context():
    print(" Создание таблиц в БД...")
    db.create_all()
    print(" Таблицы созданы!")
    
    # Создаем пользователей если нет
    if not User.query.first():
        print(" Создание тестовых пользователей...")
        admin = User(username='admin', email='admin@autosalon.ru', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        user = User(username='user', email='user@autosalon.ru', is_admin=False)
        user.set_password('user123')
        db.session.add(user)
        db.session.commit()
        print(" Пользователи созданы: admin/admin123, user/user123")
    
    print(" Инициализация завершена!")
