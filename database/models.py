from flask_sqlalchemy import SQLAlchemy
from flaskapp import app

db = SQLAlchemy(app)

class web(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)  # integer primary key will be autoincremented by default
    login = db.Column(db.String(255), unique=True, nullable=False)
    user_fname = db.Column(db.String(255))
    user_sname = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    works = db.relationship('Work', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"User(user_id {self.user_id!r}, name={self.user_fname!r}, surname={self.user_fname!r})"
