from sqlalchemy.sql import func
from app import db

user_token_assignment = db.Table(
    "user_token_assigment",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("token_id", db.Integer, db.ForeignKey("token.id"))
)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(64), nullable=False)
    permissions = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    expires_at = db.Column(db.Integer, default=-1)
    revoked = db.Column(db.Boolean, default=False)

    def __str__(self):
        return "<Token %s:%s>" % (self.key, self.value)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(64), nullable=False)
    token = db.relationship(
        "Token", 
        backref="user", 
        lazy="dynamic", 
        cascade="all,delete", 
        secondary=user_token_assignment
    )

    def __str__(self):
        return "<User %s>" % self.name