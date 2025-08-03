
from flask import Flask, render_template, jsonify
from app.routes.OTP_controller import verify_otp, otp_bp
from app.routes.cart_controller import cart_bp
from app.utils.exception import APIException
from config_email import Config_email, ConfigCart
from app.extentions import mongo, mail


def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(Config_email)

    app.config.from_object(ConfigCart)



    if testing:
        app.config["MONGO_URI"] = "mongodb://localhost:27017/ecommerce_test"
        app.config["MAIL_SUPPRESS_SEND"] = True

    mongo.init_app(app)
    mail.init_app(app)



    @app.route('/')
    def home():
        return render_template("home_page.html")

    @app.route('/verify-otp')
    def otp_page():
        return render_template('verify_otp.html')



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
    app.register_blueprint(cart_bp)

    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify(message="Resource not found"), 404

    @app.errorhandler(500)
    def handle_server_error(e):
        return jsonify(message="Internal server error"), 500

    return app
