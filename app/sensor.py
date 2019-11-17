#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/10
# @Author  : aimkiray

from app import db, ser
from app.models import Sensor

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


@bp.route('/send')
@login_required
def handle_send():
    send_data = None
    node = request.args.get('node')
    action = request.args.get('action')
    if node == 'lamp':
        if action == 'true':
            send_data = b'\xfe\x05\xa3\x44\x03\x00\x11\xff'
        else:
            send_data = b'\xfe\x05\xa3\x44\x03\x00\x10\xff'
    elif node == 'fan':
        if action == 'true':
            send_data = b'\xfe\x05\xa3\x45\x03\x00\x11\xff'
        else:
            send_data = b'\xfe\x05\xa3\x45\x03\x00\x10\xff'
    ser.on_send(send_data)
    # print("send to serial: %s" % str(send_data))
    return "True"


# Just recycle data, determine data type based on port
@ser.on_message()
def handle_message(msg):
    db.session.add(Sensor("temp", msg[6], msg[7]))
    db.session.commit()
    print("receive a message:", msg[6])


@bp.route('/read')
def show_message():
    temp = Sensor.query.order_by(Sensor.id.desc()).first()
    return jsonify({'result': 'success', 'data': temp.sensor_data})


# @ser.on_message()
# def handle_message(msg):
#     print("receive a message:", msg)
#     socketio.emit("serial_message", data={"message": str(msg)})


@ser.on_log()
def handle_logging(level, info):
    print(level, info)
