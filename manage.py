from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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


if __name__ == '__main__':
    manager.run()