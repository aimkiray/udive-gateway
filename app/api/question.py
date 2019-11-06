#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/6/2019
# @Author  : aimkiray

from app.api import bp
from app import db
from app.models import Gate
from flask import jsonify, request


@bp.route('/question/<int:id>', methods=['GET'])
def get_question(id):
    pass


@bp.route('/q/<string:topic>', methods=['GET'])
def get_answer(topic):
    question = Gate.query.filter_by(topic=topic).first()
    return jsonify({'result': 'success', 'data': question.answer})


@bp.route('/question', methods=['GET'])
def get_question_list():
    pass


@bp.route('/question', methods=['POST'])
def create_question():
    all_dict = request.get_json()
    gate = Gate(topic=all_dict.get('topic'), answer=all_dict.get('answer'), topic_raw=all_dict.get('topic_raw'),
                answer_raw=all_dict.get('answer_raw'), course=all_dict.get('course'), remark=all_dict.get('remark'),
                related_pic=all_dict.get('related_pic'), user_id=all_dict.get('user_id'))
    db.session.add(gate)
    db.session.commit()
    return jsonify({'result': 'success'})


@bp.route('/question/<int:id>', methods=['PUT'])
def update_question(id):
    pass
