
from flask import Flask, render_template, jsonify
from app.routes.OTP_controller import verify_otp, otp_bp
from config import Config
from app.extentions import mongo, mail


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.render_template = "templates"

    if testing:
        app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce_test"
        app.config["MAIL_SUPPRESS_SEND"] = True

    mongo.init_app(app)
    mail.init_app(app)



    @app.route('/')
    def home():
        return render_template("home_page.html")
    @app.route('/')
    def seller_dashboard():
        render_template("seller_dashboard.html")

    @app.route('/debug/users')
    def debug_users():
        users = list(mongo.db.users.find())
        for u in users:
            u['_id'] = str(u['_id'])
        return jsonify(users)

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
    app.register_blueprint(otp_bp)

    return app
