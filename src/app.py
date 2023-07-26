from flask import Flask
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from src.auth import auth
from src.logindetail import logind
from src.itemservice import item
from src.uploadImage import upload
from src.database import db
from src.config.swagger import template, swagger_config


app = Flask(__name__,instance_relative_config=True)
app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),

            SWAGGER={
                'title': "Ecommerce APIs",
                'uiversion': 3
            }
        )

db.app = app
db.init_app(app)
JWTManager(app)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": ["https://example.com"]}})

# add services for auth, login and item list.
app.register_blueprint(auth)
app.register_blueprint(logind)
app.register_blueprint(item)
app.register_blueprint(upload)

Swagger(app, config=swagger_config, template=template)

