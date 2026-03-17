from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    engine = db.Column(db.String(20), nullable=False)
    transmission = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Car {self.brand} {self.model}>'

class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    car_brand = db.Column(db.String(50), nullable=False)
    car_model = db.Column(db.String(50), nullable=False)
    sale_date = db.Column(db.Date, nullable=False)
    sale_price = db.Column(db.Integer, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    manager_name = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Sale {self.car_brand} {self.car_model}>'

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    preferred_car = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Customer {self.full_name}>'
