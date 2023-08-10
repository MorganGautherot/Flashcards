from . import db
from datetime import datetime

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100))
    name = db.Column('name', db.String(100))
    date_created = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    email = db.Column('email', db.String(100))
    password = db.Column('password', db.String(100))
    
    def __init__(self, email, password):
        self.email=email
        self.password=password