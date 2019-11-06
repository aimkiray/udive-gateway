#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/4
# @Author  : aimkiray

from app.forms import LoginForm, RegistrationForm, UploadForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db, photos, generate

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, jsonify, json, Response
)

bp = Blueprint('surface', __name__)


# index page
@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('surface.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('surface.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('surface.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('surface.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('surface.index'))
    form = RegistrationForm()
    if form.validate_on_submit() and form.key.data == 'awsl':
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('您已经过凉宫ハルヒ认可，成为SOS团团员与外星人，未来人，和超能力者一起玩。')
        return redirect(url_for('surface.login'))
    else:
        flash('您没有经过凉宫ハルヒ认可，不能成为SOS团团员与外星人，未来人，和超能力者一起玩。')
    return render_template('register.html', title='Register', form=form)


@bp.route('/new')
@login_required
def new():
    course_str = current_app.config['COURSE']
    course_list = course_str.split(',')
    return render_template('question/new.html', course_list=course_list)


@bp.route('/uploads', methods=['GET', 'POST'])
def uploads():
    form = UploadForm()
    if form.photo.data is not None:
        filename = photos.save(form.photo.data)
        return jsonify({'result': 'success', 'file_url': photos.url(filename), 'file_name': filename})
    else:
        return jsonify({'result': 'false'})


@bp.route('/video')
def video():
    return render_template('video.html')


@bp.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")
