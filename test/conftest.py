import sys
import os
import pytest
from flask import current_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, mongo  # ✅ import mongo directly here

@pytest.fixture
def test_client():
    app = create_app(testing=True)
    app.config['TESTING'] = True
    app.config['MAIL_SUPPRESS_SEND'] = True

    with app.test_client() as client:
        with app.app_context():
            mongo.cx.drop_database("ecommerce_test")
        yield client

@pytest.fixture(autouse=True)
def clear_users_collection(test_client):
    with test_client.application.app_context():
        mongo.db.users.delete_many({})
