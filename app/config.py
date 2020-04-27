#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5
# @Author  : aimkiray


# import os

# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_HOST = '127.0.0.1'
    DB_USER = 'umr'
    DB_PASSWORD = '12138'
    DATABASE = 'umr'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MOTION_PHOTOS_DEST = r'app/static/motion'
    SERIAL_TIMEOUT = 0.1
    SERIAL_PORT = '/dev/ttyUSB0'
    SERIAL_BAUDRATE = 115200
    SERIAL_BYTESIZE = 8
    SERIAL_PARITY = 'N'
    SERIAL_STOPBITS = 1
    PI_CAMERA = 0


class DevConfig(Config):
    SECRET_KEY = '12138'
    DEBUG = True


class ProdConfig(Config):
    SECRET_KEY = '12138'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://umr:12138@10.42.0.1/umr'
    SERIAL_PORT = '/dev/ttyAMA0'
    MOTION_PHOTOS_DEST = r'app/static/motion'
    PI_CAMERA = 1
