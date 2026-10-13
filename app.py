# -*- coding: utf-8 -*-
from flask import Flask
from flask_migrate import Migrate

from config import app_config, app_active
from extensions import db

from routes.pedidos import pedidos_bp

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__)

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(pedidos_bp)

    return app
