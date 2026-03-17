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
    
    app = Flask(__name__,
                template_folder=os.path.join(project_root, 'templates'),
                static_folder=os.path.join(project_root, 'static'))
    
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ПРИ СТАРТЕ
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created!")
            
            # Создаем тестовых пользователей если нет
            from app.models import User, Car
            if not User.query.first():
                admin = User(username='admin', email='admin@autosalon.ru', is_admin=True)
                admin.set_password('admin123')
                db.session.add(admin)
                
                user = User(username='user', email='user@autosalon.ru', is_admin=False)
                user.set_password('user123')
                db.session.add(user)
                
                # Создаем несколько тестовых автомобилей
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
                print("✅ Test data created!")
        except Exception as e:
            print(f"❌ Database init error: {e}")
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app