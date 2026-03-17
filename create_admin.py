from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Проверка существования админа
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        # Создаем админа
        admin = User(username='admin', email='admin@autosalon.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print(" Админ создан!")
        print("   Логин: admin")
        print("   Пароль: admin123")
    else:
        print("ℹ Админ уже существует")
    
    # Создаем обычного пользователя для теста
    user = User.query.filter_by(username='user').first()
    if not user:
        user = User(username='user', email='user@autosalon.com', is_admin=False)
        user.set_password('user123')
        db.session.add(user)
        db.session.commit()
        print(" Тестовый пользователь создан!")
        print("   Логин: user")
        print("   Пароль: user123")
    else:
        print("ℹ Тестовый пользователь уже существует")
