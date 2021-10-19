import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DB Models
class Users(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     public_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
     name = db.Column(db.String(50))
     password = db.Column(db.String(512))
     admin = db.Column(db.Boolean)

class Posts(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(50))
     date = db.Column(db.Date)
     author = db.Column(db.String(50))
     body = db.Column(db.String)
