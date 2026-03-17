from app import create_app, db
from app.models import Car, Sale, Customer, User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Car': Car, 'Sale': Sale, 'Customer': Customer, 'User': User}

if __name__ == '__main__':
    app.run(debug=True)
