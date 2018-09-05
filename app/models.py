from sqlalchemy.sql import func
from app import db

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(64), nullable=False)
    permissions = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    expires_at = db.Column(db.Integer, default=-1)
    revoked = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __str__(self):
        return "<Token %s:%s>" % (self.key, self.value)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False)
    tokens = db.relationship("Token", backref="user", lazy="dynamic")

    def __str__(self):
        return "<User %s>" % self.name