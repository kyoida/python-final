# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Create the SQLAlchemy instance

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    user_fname = db.Column(db.String(255))
    user_sname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
