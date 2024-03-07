from datetime import datetime

from . import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    groups = db.relationship("Group", backref="creator", lazy=True)

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}')"
