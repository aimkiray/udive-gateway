from app import db
from flask_login import UserMixin
from app import login
from datetime import datetime


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30))
    last_edit = db.Column(db.String(30))
    gates = db.relationship('Gate', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password, password

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Gate(db.Model):
    __tablename__ = 'gate'

    id = db.Column(db.BigInteger, primary_key=True)
    gmt_create = db.Column(db.DateTime)
    gmt_modified = db.Column(db.DateTime)
    course = db.Column(db.String(100))
    topic = db.Column(db.String(255))
    answer = db.Column(db.String(255))
    topic_raw = db.Column(db.Text)
    answer_raw = db.Column(db.Text)
    remark = db.Column(db.String(255))
    related_pic = db.Column(db.String(255))
    is_deleted = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.BigInteger, primary_key=True)
    gmt_create = db.Column(db.DateTime)
    gmt_modified = db.Column(db.DateTime)
    related_path = db.Column(db.String(255))

    def __init__(self, related_path, gmt_create=None, gmt_modified=None):
        self.related_path = related_path
        if gmt_create is None:
            gmt_create = datetime.utcnow()
        self.gmt_create = gmt_create
        if gmt_modified is None:
            gmt_modified = datetime.utcnow()
        self.gmt_modified = gmt_modified

    def __repr__(self):
        return '<Media %r>' % self.title
