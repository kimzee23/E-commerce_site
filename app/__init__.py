from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce_test"
    else:
        app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce"

    mongo.init_app(app)
    CORS(app)

    from app.routes.customer_controller import customer_bp
    app.register_blueprint(customer_bp)


    return app
