import os


class Config_email:
    MONGO_URI = "mongodb://localhost:27017/ecommerce_store"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'gazartechnology@gmail.com'
    MAIL_PASSWORD = 'mxnd svdh hhbk jfxe'
    MAIL_DEFAULT_SENDER = 'gazartechnology@gmail.com'


class ConfigCart:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/ecommerce_store')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-me')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

    # Cart settings
    MAX_CART_ITEMS = 50
    MAX_QUANTITY_PER_ITEM = 10
    DEFAULT_CURRENCY = 'USD'