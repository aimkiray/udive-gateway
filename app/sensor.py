#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/10
# @Author  : aimkiray

from app import db, ser
from app.models import Sensor, Config

from flask_login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json, Response
)

bp = Blueprint('sensor', __name__)


@bp.route('/switch')
@login_required
def switch():
    temp_first = Sensor.query.order_by(Sensor.id.desc()).first()
    config_list = Config.query.all()
    # status = {}
    # for config in config_list:
    #     status.pop(config.sensor_type, config.status)
    return render_template('sensor.html', temp_first=temp_first.sensor_data, config_list=config_list)


# @socketio.on('send')
# @login_required
# def handle_send(json_str):
#     data = json.loads(json_str)
#     ser.on_send(data['message'])
#     print("send to serial: %s" % data['message'])


@bp.route('/send')
@login_required
def handle_send():
    # Zigbee communication dedicated instruction
    send_data = None
    # Node working status
    status = None
    node = request.args.get('node')
    action = request.args.get('action')
    if node == 'lamp':
        if action == 'true':
            send_data = b'\xfe\x05\xa3\x44\x03\x00\x11\xff'
            status = 1
        else:
            send_data = b'\xfe\x05\xa3\x44\x03\x00\x10\xff'
            status = 0
    elif node == 'fan0':
        if action == 'true':
            send_data = b'\xfe\x05\xa3\x45\x03\x00\x11\xff'
            status = 1
        else:
            send_data = b'\xfe\x05\xa3\x45\x03\x00\x10\xff'
            status = 0
    if send_data and status is not None:
        ser.on_send(send_data)
        config = Config.query.filter_by(sensor_type=node).first()
        # Automatic operation is 0, and manual is 1
        config.where = 1
        config.status = status
        db.session.commit()
    return "True"


# Just recycle data, determine data type based on port
@ser.on_message()
def handle_message(msg):
    now_temp = msg[6]
    temp_config = Config.query.filter_by(sensor_type='temp').first()
    fan0_config = Config.query.filter_by(sensor_type='fan0').first()
    # Temperature is too high
    if now_temp > temp_config.max_value:
        if fan0_config.status == 0:
            # Turn on fan0
            ser.on_send(b'\xfe\x05\xa3\x45\x03\x00\x11\xff')
            # Automatic operation is 0, and manual is 1
            fan0_config.where = 0
            fan0_config.status = 1
    else:
        if fan0_config.status == 1 and fan0_config.where == 0:
            # Turn off fan0
            ser.on_send(b'\xfe\x05\xa3\x45\x03\x00\x10\xff')
            fan0_config.status = 0

    db.session.add(Sensor("temp", now_temp, msg[7]))
    db.session.commit()


@bp.route('/read')
@login_required
def show_message():
    temp = Sensor.query.order_by(Sensor.id.desc()).first()
    return jsonify({'result': 'success', 'data': temp.sensor_data})


@bp.route('/set_value')
@login_required
def set_value():
    min_value = request.args.get('min_value')
    max_value = request.args.get('max_value')
    # status = request.args.get('status')
    config = Config.query.filter_by(sensor_type='temp').first()
    if max_value > min_value:
        config.min_value = min_value
        config.max_value = max_value
        # config.status = status
        db.session.commit()
        return "True"
    else:
        return "False"


# @ser.on_message()
# def handle_message(msg):
#     print("receive a message:", msg)
#     socketio.emit("serial_message", data={"message": str(msg)})


@ser.on_log()
def handle_logging(level, info):
    print(level, info)
