#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/6/2019
# @Author  : aimkiray


from app.forms import LoginForm

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json
)

bp = Blueprint('question', __name__)


# get question from request
@bp.route('/q')
def get():
    id_list = request.args.get('rawIds').split(',')
    return 0


# modify question
@bp.route('/q', methods=['POST'])
def post():
    all_dict = request.get_json()
    item_state_dict = all_dict.get('item_dict')
    request_status_dict = all_dict.get('request_dict')
    user_dict = all_dict.get('user_dict')
    sql_remove_all = current_app.config['SQL_REMOVE_ALL']
    sql_remove_invoiced = current_app.config['SQL_REMOVE_INVOICED']
    return jsonify({'result': 'success'})
