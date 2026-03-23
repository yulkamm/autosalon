import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sprinthost-change-this-secret-key'
    
    # SQLite в домашней директории SprintHost
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.expanduser('~'), 'car_dealership.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
