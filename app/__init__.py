#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/4
# @Author  : aimkiray

import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
# from flask_wtf.csrf import CSRFProtect
from app.serial import Serial
from flask_socketio import SocketIO
import configparser

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
photos = UploadSet('photos', IMAGES)
ser = Serial()
socketio = SocketIO()
# csrf = CSRFProtect()

config = configparser.ConfigParser()
config.read('config.ini')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.' + config['DEFAULT']['Env'] + 'Config')

    bootstrap.init_app(app)
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    ser.init_app(app)
    socketio.init_app(app)
    login.login_view = 'surface.login'
    # file
    configure_uploads(app, photos)
    patch_request_class(app, app.config['MAX_CONTENT_LENGTH'])  # set maximum file size, default is 16MB
    # csrf.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # routes
    from app import surface
    app.register_blueprint(surface.bp)

    from app import camera
    app.register_blueprint(camera.bp)

    from app import sensor
    app.register_blueprint(sensor.bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
