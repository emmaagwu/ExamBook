from decouple import config
import os


class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    MAIL_SERVER = config('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = config('MAIL_PORT', 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER', 'noreply@example.com')
    UPLOAD_FOLDER = os.path.join(os.getcwd(), config('UPLOAD_FOLDER', 'uploads/avatars'))
    ALLOWED_EXTENSIONS = set(config('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))
    UPLOAD_PATH = config('UPLOAD_PATH', 'uploads/avatars')

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    DEBUG = True

config_dict = {
    'dev': DevConfig
}
