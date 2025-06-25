import pytest
from flask import Flask, current_app
from flask_pymongo import pymongo, PyMongo
from app import create_app

@pytest.fixture
def test_client():
    app = create_app(testing=True)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
    mongo = PyMongo(app)
    app.mongo = mongo

    with app.test_client() as test_client:
        with app.app_context():
            mongo.db.user.delete_many({})
            yield test_client


@pytest.fixture(autouse=True)
def clear_users_collection(test_client):
    with test_client.application.app_context():
        mongo = current_app.mongo
        mongo.db.users.delete_many({})
