from app import create_app, db
from app.models import User, Car, Sale, Customer
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    print(" Создание таблиц...")
    db.create_all()
    
    # Создаем пользователей только если их нет
    if not User.query.first():
        print(" Создание пользователей...")
        admin = User(username='admin', email='admin@autosalon.ru', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        user = User(username='user', email='user@autosalon.ru', is_admin=False)
        user.set_password('user123')
        db.session.add(user)
        db.session.commit()
        
        brands = ['Toyota', 'BMW', 'Mercedes', 'Audi', 'Lexus', 'Honda', 'Nissan']
        models = {
            'Toyota': ['Camry', 'Corolla', 'RAV4'],
            'BMW': ['X5', '3 Series', '5 Series'],
            'Mercedes': ['C-Class', 'E-Class', 'GLE'],
            'Audi': ['A4', 'A6', 'Q5'],
            'Lexus': ['RX', 'ES', 'NX'],
            'Honda': ['Civic', 'Accord', 'CR-V'],
            'Nissan': ['Altima', 'Maxima', 'Rogue']
        }
        colors = ['Белый', 'Черный', 'Серебристый', 'Серый', 'Красный', 'Синий']
        engines = ['2.0L', '2.5L', '3.0L', '3.5L V6']
        transmissions = ['Автомат', 'Механика', 'Вариатор']
        payment_methods = ['Наличные', 'Банковская карта', 'Кредит', 'Лизинг']
        
        first_names = ['Александр', 'Михаил', 'Дмитрий', 'Иван', 'Сергей', 'Елена', 'Ольга', 'Наталья', 'Татьяна', 'Мария']
        last_names = ['Иванов', 'Петров', 'Сидоров', 'Козлов', 'Волков', 'Смирнов', 'Иванова', 'Петрова', 'Сидорова', 'Козлова']
        manager_names = ['Александр Петров', 'Иван Сидоров', 'Мария Иванова', 'Елена Козлова', 'Дмитрий Волков']
        
        # Генерация 100 автомобилей
        print(" Генерация 100 автомобилей...")
        for i in range(1, 101):
            brand = random.choice(brands)
            car = Car(
                brand=brand,
                model=random.choice(models[brand]),
                year=random.randint(2015, 2026),
                price=random.randint(500000, 8500000),
                color=random.choice(colors),
                mileage=random.randint(0, 150000),
                engine=random.choice(engines),
                transmission=random.choice(transmissions),
                photo=f'tables/cars/car_{((i-1) % 10) + 1}.jpg'
            )
            db.session.add(car)
        
        # Генерация 100 продаж
        print(" Генерация 100 продаж...")
        for i in range(1, 101):
            brand = random.choice(brands)
            sale = Sale(
                car_brand=brand,
                car_model=random.choice(models[brand]),
                sale_date=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                sale_price=random.randint(500000, 8500000),
                customer_name=f'{random.choice(first_names)} {random.choice(last_names)}',
                customer_phone=f'+7 ({random.randint(900,999)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
                manager_name=random.choice(manager_names),
                payment_method=random.choice(payment_methods),
                photo=f'tables/sales/sale_{((i-1) % 10) + 1}.jpg'
            )
            db.session.add(sale)
        
        # Генерация 10 менеджеров
        print(" Генерация 10 менеджеров...")
        for i in range(1, 11):
            customer = Customer(
                full_name=f'{random.choice(first_names)} {random.choice(last_names)}',
                phone=f'+7 ({random.randint(900,999)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
                email=f'manager{i}@autosalon.ru',
                address=f'г. Москва, ул. Тверская, д. {i}',
                birth_date=datetime.utcnow() - timedelta(days=random.randint(7300, 25550)),
                preferred_car=random.choice(['Седан', 'Внедорожник', 'Кроссовер', 'Хэтчбек']),
                status=random.choice(['Активен', 'VIP', 'Постоянный', 'Новый']),
                photo=f'pages/contacts/manager_{i}.jpg'
            )
            db.session.add(customer)
        
        db.session.commit()
        print(" База данных успешно инициализирована!")
        print("   Админ: admin / admin123")
        print("   Пользователь: user / user123")
    else:
        print(" База данных уже инициализирована")
