#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5
# @Author  : aimkiray


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DB_HOST = '127.0.0.1'
    DB_USER = 'umr'
    DB_PASSWORD = '12138'
    DATABASE = 'umr'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://umr:12138@127.0.0.1/umr'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    COURSE = 'gc,xh,cy,dl,cg,mn,sz'
    UPLOADED_PHOTOS_DEST = r'C:\Users\savant\Dropbox\Projects\Python\umr\app\static\uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


class DevConfig(Config):
    SECRET_KEY = '12138'
    DEBUG = True


class ProdConfig(Config):
    SECRET_KEY = '12138'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://umr:awsl12138@127.0.0.1/umr'
    UPLOADED_PHOTOS_DEST = r'C:\Users\Administrator\Desktop\Project\umr\app\static\uploads'
