from . import db
from flask_login import UserMixin


class Protein(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    daily_protein = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.Float, nullable=False)
    percent = db.Column(db.Float, nullable=False)
    remaining_value = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    user_input = db.relationship('Protein')
    user_goal = db.relationship("Goal")
