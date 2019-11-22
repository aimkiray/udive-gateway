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


class Camera(db.Model):
    __tablename__ = 'camera'

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
        return '<Screenshot %r>' % self.related_path


# TODO Many to One --> Config
class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.BigInteger, primary_key=True)
    gmt_create = db.Column(db.DateTime)
    gmt_modified = db.Column(db.DateTime)
    sensor_type = db.Column(db.String(100))
    sensor_data = db.Column(db.BigInteger)
    others = db.Column(db.String(100))

    def __init__(self, sensor_type, sensor_data, others=None, gmt_create=None, gmt_modified=None):
        self.sensor_type = sensor_type
        self.sensor_data = sensor_data
        self.others = others
        if gmt_create is None:
            gmt_create = datetime.utcnow()
        self.gmt_create = gmt_create
        if gmt_modified is None:
            gmt_modified = datetime.utcnow()
        self.gmt_modified = gmt_modified

    def __repr__(self):
        return '<Sensor %r>' % self.sensor_type


class Config(db.Model):
    __tablename__ = 'config'

    id = db.Column(db.BigInteger, primary_key=True)
    gmt_create = db.Column(db.DateTime)
    gmt_modified = db.Column(db.DateTime)
    sensor_type = db.Column(db.String(100))
    min_value = db.Column(db.BigInteger)
    max_value = db.Column(db.BigInteger)
    status = db.Column(db.Integer)
    others = db.Column(db.String(100))
    disabled = db.Column(db.Integer)
    where = db.Column(db.Integer)

    def __init__(self, sensor_type, status=None, min_value=None, max_value=None, others=None, gmt_create=None,
                 gmt_modified=None):
        self.sensor_type = sensor_type
        self.min_value = min_value
        self.max_value = max_value
        self.status = status
        self.others = others
        if gmt_create is None:
            gmt_create = datetime.utcnow()
        self.gmt_create = gmt_create
        if gmt_modified is None:
            gmt_modified = datetime.utcnow()
        self.gmt_modified = gmt_modified

    def __repr__(self):
        return '<Config %r>' % self.sensor_type
