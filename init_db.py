from app import create_app, db
from app.models import User, Car, Sale, Customer
from datetime import datetime, timedelta
import random

app = create_app()

with app.app_context():
    print("=" * 50)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    print("\n Создание таблиц...")
    db.drop_all()
    db.create_all()
    print(" Таблицы созданы!")
    
    # Создаем админа
    admin = User(username='admin', email='admin@autosalon.ru', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Создаем обычного пользователя
    user = User(username='user', email='user@autosalon.ru', is_admin=False)
    user.set_password('user123')
    db.session.add(user)
    db.session.commit()
    print(" Пользователи созданы!")
    print("   Админ: admin / admin123")
    print("   Пользователь: user / user123")
    
    # Русские данные
    brands = ['Toyota', 'BMW', 'Mercedes', 'Audi', 'Lexus', 'Honda', 'Nissan', 'Mazda', 'Kia', 'Hyundai']
    models = {
        'Toyota': ['Camry', 'Corolla', 'RAV4', 'Land Cruiser'],
        'BMW': ['X5', '3 Series', '5 Series', 'X7'],
        'Mercedes': ['C-Class', 'E-Class', 'GLE', 'S-Class'],
        'Audi': ['A4', 'A6', 'Q5', 'Q7'],
        'Lexus': ['RX', 'ES', 'NX', 'LX'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot'],
        'Nissan': ['Altima', 'Maxima', 'Rogue', 'Pathfinder'],
        'Mazda': ['Mazda3', 'Mazda6', 'CX-5', 'CX-9'],
        'Kia': ['Optima', 'Sorento', 'Sportage', 'Telluride'],
        'Hyundai': ['Sonata', 'Tucson', 'Santa Fe', 'Palisade']
    }
    colors = ['Белый', 'Черный', 'Серебристый', 'Серый', 'Красный', 'Синий', 'Зеленый', 'Коричневый']
    engines = ['2.0L', '2.5L', '3.0L', '3.5L V6', '4.0L V8', '1.6L Turbo', '2.4L Hybrid']
    transmissions = ['Автомат', 'Механика', 'Вариатор', 'Робот']
    payment_methods = ['Наличные', 'Банковская карта', 'Банковский перевод', 'Кредит', 'Лизинг']
    
    first_names = ['Александр', 'Михаил', 'Дмитрий', 'Иван', 'Сергей', 'Андрей', 'Алексей', 'Владимир', 'Николай', 'Павел',
                   'Елена', 'Ольга', 'Наталья', 'Татьяна', 'Мария', 'Анна', 'Светлана', 'Ирина', 'Юлия', 'Екатерина']
    last_names = ['Иванов', 'Петров', 'Сидоров', 'Козлов', 'Волков', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Соколов',
                  'Иванова', 'Петрова', 'Сидорова', 'Козлова', 'Волкова', 'Смирнова', 'Кузнецова', 'Попова', 'Васильева', 'Соколова']
    
    manager_names = ['Александр Петров', 'Иван Сидоров', 'Мария Иванова', 'Елена Козлова', 'Дмитрий Волков', 
                     'Анна Смирнова', 'Сергей Кузнецов']
    
    # Генерация 100 автомобилей (10 фото распределяются на 100 записей)
    print("\n Генерация 100 автомобилей (10 фото распределяются автоматически)...")
    cars = []
    for i in range(1, 101):
        brand = random.choice(brands)
        model = random.choice(models[brand])
        # Автоматическое распределение: 10 фото на 100 записей (каждое фото используется 10 раз)
        photo_num = ((i - 1) % 10) + 1  # 1,2,3,4,5,6,7,8,9,10,1,2,3...
        car = Car(
            brand=brand,
            model=model,
            year=random.randint(2015, 2026),
            price=random.randint(500000, 8500000),
            color=random.choice(colors),
            mileage=random.randint(0, 150000),
            engine=random.choice(engines),
            transmission=random.choice(transmissions),
            photo=f'tables/cars/car_{photo_num}.jpg'
        )
        cars.append(car)
    db.session.bulk_save_objects(cars)
    db.session.commit()
    print(f" Автомобилей: {Car.query.count()}")
    print("    10 фото автоматически распределены на 100 записей")
    
    # Генерация 100 продаж (10 фото распределяются на 100 записей)
    print("\n Генерация 100 продаж (10 фото распределяются автоматически)...")
    sales = []
    for i in range(1, 101):
        brand = random.choice(brands)
        model = random.choice(models[brand])
        first = random.choice(first_names)
        last = random.choice(last_names)
        days_ago = random.randint(1, 365)
        # Автоматическое распределение: 10 фото на 100 записей
        photo_num = ((i - 1) % 10) + 1
        sale = Sale(
            car_brand=brand,
            car_model=model,
            sale_date=datetime.utcnow() - timedelta(days=days_ago),
            sale_price=random.randint(500000, 8500000),
            customer_name=f'{first} {last}',
            customer_phone=f'+7 ({random.randint(900,999)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
            manager_name=random.choice(manager_names),
            payment_method=random.choice(payment_methods),
            photo=f'tables/sales/sale_{photo_num}.jpg'
        )
        sales.append(sale)
    db.session.bulk_save_objects(sales)
    db.session.commit()
    print(f" Продаж: {Sale.query.count()}")
    print("    10 фото автоматически распределены на 100 записей")
    
    # Генерация 10 клиентов (менеджеров для страницы контактов)
    print("\n Генерация 10 менеджеров...")
    customers = []
    for i in range(1, 11):
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        customer = Customer(
            full_name=f'{first} {last}',
            phone=f'+7 ({random.randint(900,999)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
            email=f'{first.lower()}.{last.lower()}@autosalon.ru',
            address=f'г. Москва, ул. Тверская, д. {i}',
            birth_date=datetime.utcnow() - timedelta(days=random.randint(7300, 25550)),
            registration_date=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            preferred_car=random.choice(['Седан', 'Внедорожник', 'Кроссовер', 'Хэтчбек']),
            status=random.choice(['Активен', 'VIP', 'Постоянный', 'Новый']),
            photo=f'pages/contacts/manager_{i}.jpg'
        )
        customers.append(customer)
    db.session.bulk_save_objects(customers)
    db.session.commit()
    print(f" Менеджеров: {Customer.query.count()}")
    
    print("\n" + "=" * 50)
    print(" БАЗА ДАННЫХ ГОТОВА!")
    print("=" * 50)
    print("\n СТРУКТУРА ФОТО:")
    print("    static/images/pages/cars/ - car_1.jpg, car_2.jpg, car_3.jpg (3 фото)")
    print("    static/images/pages/about/ - about_1.jpg ... about_5.jpg (5 фото)")
    print("    static/images/pages/contacts/ - manager_1.jpg ... manager_10.jpg (10 фото)")
    print("    static/images/tables/cars/ - car_1.jpg ... car_10.jpg (10 фото на 100 записей)")
    print("    static/images/tables/sales/ - sale_1.jpg ... sale_10.jpg (10 фото на 100 записей)")
