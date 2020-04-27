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
# from flask_wtf.csrf import CSRFProtect
# from app.serial import Serial
from app.opencv import OpenCV
# from flask_socketio import SocketIO

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
# ser = Serial()
cv = OpenCV()
# socketio = SocketIO()
# csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.' + os.environ.get('Env') + 'Config')

    bootstrap.init_app(app)
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    # ser.init_app(app)
    cv.init_app(app)
    # socketio.init_app(app)
    login.login_view = 'surface.login'
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

    # from app import sensor
    # app.register_blueprint(sensor.bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
