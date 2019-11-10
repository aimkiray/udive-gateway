#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/10
# @Author  : aimkiray

from app import db, ser

from flask_login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json, Response
)

bp = Blueprint('sensor', __name__)


@bp.route('/switch')
@login_required
def switch():
    return render_template('sensor.html')


# @socketio.on('send')
# @login_required
# def handle_send(json_str):
#     data = json.loads(json_str)
#     ser.on_send(data['message'])
#     print("send to serial: %s" % data['message'])

# 数据一共四位，分别是
@bp.route('/send')
@login_required
def handle_send():
    send_data = None
    node = request.args.get('node')
    if node == 'lamp':
        send_data = b'\xfe\x08\xaa\xaa\x02\x00\x01\x02\x03\x04\xff'
    elif node == 'fan':
        send_data = b'\xfe\x08\xaa\xaa\x02\x00\x01\x02\x03\x04\xff'
    ser.on_send(send_data)
    print("send to serial: %s" % str(send_data))
    return "True"


# Just recycle data, determine data type based on address
@ser.on_message()
def handle_message(msg):
    print("receive a message:", msg)


# @ser.on_message()
# def handle_message(msg):
#     print("receive a message:", msg)
#     socketio.emit("serial_message", data={"message": str(msg)})


@ser.on_log()
def handle_logging(level, info):
    print(level, info)
