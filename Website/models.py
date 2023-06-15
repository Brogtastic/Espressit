from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz
from PIL import Image

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('EST')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(100))
    title = db.Column(db.String(25))

    @property
    def noteLength(self):
        length = len(self.data)
        if (len(self.data) > 200): length = length/1.68
        elif (len(self.data) > 390): length = length / 1.66 + 10
        else: length = length/1.8
        return length + 180
    
    @property
    def imageWidth(self):
        width = self.image.width
        return width

    @property
    def imageHeight(self):
        height = self.image.height
        return height


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')