from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://umr:12138@127.0.0.1/umr'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30))
    others = db.Column(db.String(30))

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password, password

    def __repr__(self):
        return '<User {}>'.format(self.username)


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
        return '<Camera %r>' % self.title


class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.BigInteger, primary_key=True)
    gmt_create = db.Column(db.DateTime)
    gmt_modified = db.Column(db.DateTime)
    sensor_type = db.Column(db.String(100))
    sensor_data = db.Column(db.BigInteger)
    others = db.Column(db.String(100))

    def __init__(self, related_path, gmt_create=None, gmt_modified=None):
        self.related_path = related_path
        if gmt_create is None:
            gmt_create = datetime.utcnow()
        self.gmt_create = gmt_create
        if gmt_modified is None:
            gmt_modified = datetime.utcnow()
        self.gmt_modified = gmt_modified

    def __repr__(self):
        return '<Sensor %r>' % self.title


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


if __name__ == '__main__':
    manager.run()
