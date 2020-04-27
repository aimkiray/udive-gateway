#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/4
# @Author  : aimkiray

from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db

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
        user = User()
        user.set_username(form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('您已通过鹳狸猿认证。')
        return redirect(url_for('surface.login'))
    else:
        flash('您还没有通过鹳狸猿认证，我们不能一起玩。')
    return render_template('register.html', title='Register', form=form)
