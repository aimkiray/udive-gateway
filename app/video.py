#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/6
# @Author  : aimkiray

from app.opencv import generate
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json, Response
)

bp = Blueprint('video', __name__)


@bp.route('/video')
def video():
    return render_template('video.html')


@bp.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
