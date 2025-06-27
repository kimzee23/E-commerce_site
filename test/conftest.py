import pytest
from flask import current_app
from app import create_app, mongo

@pytest.fixture
def test_client():
    app = create_app(testing=True)
    app.mongo = mongo

    with app.test_client() as client:
        with app.app_context():
            mongo.cx.drop_database("ecommerce_test")
        yield client


@pytest.fixture(autouse=True)
def clear_users_collection(test_client):
    with test_client.application.app_context():
        mongo = current_app.mongo
        mongo.db.users.delete_many({})
