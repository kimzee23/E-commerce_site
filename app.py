from flask import Flask
from app import create_app, mongo

app = Flask(__name__)


app = create_app(app)

app.mongo = mongo
if __name__ == '__main__':
    app.run()
