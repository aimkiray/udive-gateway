#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/6
# @Author  : aimkiray

from app import db
from app.models import Camera
from app.opencv import generate, get_path, reset_path

from flask_paginate import Pagination, get_page_parameter
from flask_login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json, Response
)

bp = Blueprint('camera', __name__)


@bp.route('/video')
@login_required
def video():
    return render_template('camera/video.html')


@bp.route("/video_feed")
@login_required
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@bp.route("/motion_detection")
@login_required
def motion_detection():
    path = get_path()
    if path is not None:
        path = path.split('app')[1]
        db.session.add(Camera(path))
        db.session.commit()
        reset_path()
        return "True"
    else:
        return "False"


@bp.route("/reset_motion")
@login_required
def reset_motion():
    reset_path()


@bp.route("/list_motion")
@login_required
def list_motion():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    motions = Camera.query.all()
    pagination = Pagination(page=page, total=len(motions), search=search, record_name='motions')
    return render_template("camera/list_motion.html", motions=motions, pagination=pagination)


@bp.route("/del_motion/<int:id>", methods=['DELETE'])
@login_required
def del_motion(id):
    pass
