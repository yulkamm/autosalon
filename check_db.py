from app import create_app, db
from app.models import Car, Customer

app = create_app()

with app.app_context():
    print("=" * 50)
    print("DATABASE CHECK")
    print("=" * 50)
    
    cars_count = Car.query.count()
    customers_count = Customer.query.count()
    
    print(f"\nCars in DB: {cars_count}")
    print(f"Customers in DB: {customers_count}")
    
    print("\nFirst 5 cars:")
    cars = Car.query.limit(5).all()
    for car in cars:
        print(f"   {car.brand} {car.model} ({car.year}) - ${car.price} - Photo: {car.photo}")
    
    print("\nFirst 5 customers:")
    customers = Customer.query.limit(5).all()
    for cust in customers:
        print(f"   {cust.full_name} - {cust.phone} - Photo: {cust.photo}")
    
    print("\nUnique car photos:")
    car_photos = db.session.query(Car.photo).distinct().all()
    for photo in car_photos:
        print(f"   {photo[0]}")
    
    print("\nUnique contact photos:")
    contact_photos = db.session.query(Customer.photo).distinct().all()
    for photo in contact_photos:
        print(f"   {photo[0]}")
