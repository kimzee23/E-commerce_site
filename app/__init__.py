
from flask import Flask
from config import Config
from app.extentions import mongo, mail



def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)

    if testing:
        app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce_test"
        app.config["MAIL_SUPPRESS_SEND"] = True

    mongo.init_app(app)
    mail.init_app(app)


    from app.routes.admin_controller import admin_bp
    from app.routes.super_admin_controller import superAdmin_bp
    from app.routes.seller_controller import seller_bp
    from app.routes.product_controller import product_bp
    from app.routes.product_tracker_controller import product_tracker_bp
    from app.routes.customer_controller import customer_bp
    from app.routes.chat_controller import chat_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(superAdmin_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(product_tracker_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(chat_bp)

    return app
