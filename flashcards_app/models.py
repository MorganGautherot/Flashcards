from . import db
from datetime import datetime


class Workout(db.Model):
    date_posted = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    workout_done = db.Column(db.Boolean)
    comment = db.Column(db.Text)