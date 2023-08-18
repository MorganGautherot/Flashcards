from . import db
from datetime import datetime

class users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column("date_created", db.DateTime, default=datetime.now())
    last_lesson = db.Column("last_lesson", db.Integer)
    email = db.Column('email', db.String(100))
    
    def __init__(self, email, last_lesson):
        self.last_lesson=last_lesson
        self.email=email
        self.date_created=datetime.now()

class question(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column("date_created", db.DateTime, default=datetime.now())
    question = db.Column('question', db.String(500))
    answer = db.Column('answer', db.String(500))

    def __init__(self, question, answer, lesson):
        self.question=question
        self.answer=answer
        self.lesson=lesson
        self.date_created=datetime.now()

class learning(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer)
    question_id = db.Column('question_id', db.Integer)
    next_show = db.Column("next_show", db.DateTime, default=datetime.now())

    def __init__(self, user_id, question_id):
        self.user_id=user_id
        self.question_id=question_id
        self.next_show=datetime.now()