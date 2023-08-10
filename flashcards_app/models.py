from . import db
from datetime import datetime

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column("date_created", db.DateTime, default=datetime.utcnow)
    last_lesson = db.Column("last_lesson", db.Integer)
    email = db.Column('email', db.String(100))
    
    def __init__(self, email, last_lesson):
        if last_lesson=='':
            self.last_lesson = 1
        else :
            self.last_lesson=last_lesson
        self.email=email
        self.date_created=datetime.utcnow()