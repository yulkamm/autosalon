import random
from datetime import datetime, timedelta
from app import db, create_app
from app.models import Car, Customer

def populate_database():
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
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
        colors = ['White', 'Black', 'Silver', 'Gray', 'Red', 'Blue', 'Green', 'Brown']
        engines = ['2.0L', '2.5L', '3.0L', '3.5L V6', '4.0L V8', '1.6L Turbo', '2.4L Hybrid']
        transmissions = ['Automatic', 'Manual', 'CVT', 'DCT']
        statuses = ['Active', 'VIP', 'Regular', 'New', 'Pending']
        preferred_cars = ['Sedan', 'SUV', 'Coupe', 'Hatchback', 'Truck']
        
        cars = []
        for i in range(100):
            brand = random.choice(brands)
            model = random.choice(models[brand])
            car = Car(
                brand=brand, model=model,
                year=random.randint(2015, 2026),
                price=random.randint(15000, 85000),
                color=random.choice(colors),
                mileage=random.randint(0, 150000),
                engine=random.choice(engines),
                transmission=random.choice(transmissions),
                photo=f'cars/car_{random.randint(1, 10)}.jpg'
            )
            cars.append(car)
        
        db.session.bulk_save_objects(cars)
        
        first_names = ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Richard', 'Joseph', 'Thomas', 'Charles']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        
        customers = []
        for i in range(100):
            first = random.choice(first_names)
            last = random.choice(last_names)
            days_ago = random.randint(1, 365)
            birth_days_ago = random.randint(7300, 25550)
            
            customer = Customer(
                full_name=f'{first} {last}',
                phone=f'+1-{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}',
                email=f'{first.lower()}.{last.lower()}{random.randint(1,99)}@email.com',
                address=f'{random.randint(1,9999)} {random.choice(["Main", "Oak", "Maple", "Cedar", "Pine"])} St, City',
                birth_date=datetime.utcnow() - timedelta(days=birth_days_ago),
                registration_date=datetime.utcnow() - timedelta(days=days_ago),
                preferred_car=random.choice(preferred_cars),
                status=random.choice(statuses),
                photo=f'contacts/contact_{random.randint(1, 10)}.jpg'
            )
            customers.append(customer)
        
        db.session.bulk_save_objects(customers)
        db.session.commit()
        
        print(" Database populated:")
        print(f"   - Cars: {Car.query.count()}")
        print(f"   - Customers: {Customer.query.count()}")

if __name__ == '__main__':
    populate_database()
