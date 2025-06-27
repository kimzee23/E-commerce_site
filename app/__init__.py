from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

from app.routes.admin_controller import admin_bp
from app.routes.seller_controller import seller_bp
from app.routes.super_admin_controller import superAdmin_bp

mongo = PyMongo()

def create_app(testing=False):
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce_test" if testing else "mongodb://localhost:27017/ecommerce"




    mongo.init_app(app)
    app.mongo = mongo

    from app.routes.customer_controller import customer_bp
    app.register_blueprint(customer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(superAdmin_bp)

    CORS(app)
    return app
