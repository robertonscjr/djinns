from flask import Flask, request
from flask_cors import CORS

import pymongo


def create_db(credential):
    db = pymongo.MongoClient(
            credential
        )

    return db


def create_app(app_name, blueprints):
    app = Flask(app_name)
    cors = CORS(app)
    
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
