#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/5
# @Author  : aimkiray
#
# flask-sqlacodegen --outfile modelstest.py  --flask mysql+pymysql://umr:12138@127.0.0.1/umr

import pymysql
import logging

from flask import current_app, g


def get_db():
    if 'db' not in g:
        try:
            g.db = pymysql.connect(
                current_app.config['DB_HOST'],
                current_app.config['DB_USER'],
                current_app.config['DB_PASSWORD'],
                current_app.config['DATABASE'],
                cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            logging.error("Could not connect to database: %s" % e)
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()