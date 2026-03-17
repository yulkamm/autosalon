import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'

def create_app(config_class=Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(basedir)
    
    print(f"Base dir: {basedir}", flush=True)
    print(f"Project root: {project_root}", flush=True)
    
    app = Flask(__name__,
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    
    app.config.from_object(config_class)
    
    # ПРОВЕРКА какой БД используем
    print(f"DATABASE_URL: {app.config.get('SQLALCHEMY_DATABASE_URI')}", flush=True)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Импортируем ВСЕ модели ДО создания таблиц
    from app.models import User, Car, Sale, Customer
    
    # Инициализация БД
    with app.app_context():
        try:
            print("Creating tables...", flush=True)
            db.create_all()
            print("✅ Tables created!", flush=True)
            
            # Проверяем пользователей
            try:
                user_count = User.query.count()
                print(f"Users in DB: {user_count}", flush=True)
            except Exception as check_error:
                print(f"Warning checking users: {check_error}", flush=True)
                user_count = 0
            
            if user_count == 0:
                print("Creating test users...", flush=True)
                admin = User(username='admin', email='admin@autosalon.ru', is_admin=True)
                admin.set_password('admin123')
                db.session.add(admin)
                
                user = User(username='user', email='user@autosalon.ru', is_admin=False)
                user.set_password('user123')
                db.session.add(user)
                
                # Создаем тестовые автомобили
                import random
                brands = ['Toyota', 'BMW', 'Mercedes']
                for i in range(3):
                    car = Car(
                        brand=brands[i],
                        model='Model ' + str(i+1),
                        year=2023,
                        price=2000000,
                        color='White',
                        mileage=1000,
                        engine='2.5L',
                        transmission='Автомат',
                        photo='tables/cars/car_1.jpg'
                    )
                    db.session.add(car)
                
                db.session.commit()
                print("✅ Test data created!", flush=True)
            else:
                print("✅ Users already exist!", flush=True)
                
        except Exception as e:
            print(f"❌ Database init error: {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    print("Flask app created and blueprints registered!", flush=True)
    
    return app