
from flask import Flask
from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_cors import CORS


mail = Mail()
mongo = PyMongo()

def create_app(testing=False):
    app = Flask(__name__)

    app.config["MONGO_URI"] = (
        "mongodb://localhost:27017/ecommerce_test"
        if testing else "mongodb://localhost:27017/ecommerce"
    )

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your_app_password'
    app.config['MAIL_DEFAULT_SENDER'] = 'gazartech@gmail.com'

    mongo.init_app(app)
    mail.init_app(app)

    from app.routes.customer_controller import customer_bp
    from app.routes.seller_controller import seller_bp
    from app.routes.admin_controller import admin_bp
    from app.routes.super_admin_controller import superAdmin_bp
    from app.routes.product_controller import product_bp
    from app.routes.chat_controller import chat_bp
    from app.routes.product_tracker_controller import product_tracker_bp
    from app.routes.OTP_controller import otp_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(superAdmin_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(product_tracker_bp)
    app.register_blueprint(otp_bp)

    CORS(app)
    return app