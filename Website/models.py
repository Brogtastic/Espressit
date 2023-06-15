from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz
from io import BytesIO
from PIL import Image, ExifTags

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
    def imageHeight(self):
        if self.image:
            img = Image.open('Website/static/uploads/' + self.image)
            width, height = img.size

            # Check for rotation information in EXIF metadata
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif_data = img._getexif()
            if exif_data is not None:
                exif = dict(exif_data.items())
                if orientation in exif:
                    if exif[orientation] == 6 or exif[orientation] == 8:
                        # Swap width and height if the image is rotated 90 or 270 degrees
                        height, width = width, height

            return height
        else:
            return 0

    @property
    def imageWidth(self):
        if self.image:
            img = Image.open('Website/static/uploads/' + self.image)
            width, height = img.size

            # Check for rotation information in EXIF metadata
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif_data = img._getexif()
            if exif_data is not None:
                exif = dict(exif_data.items())
                if orientation in exif:
                    if exif[orientation] == 6 or exif[orientation] == 8:
                        # Swap width and height if the image is rotated 90 or 270 degrees
                        width, height = height, width

            return width
        else:
            return 0

    @property
    def horizontal(self):
        img = Image.open('static/uploads/'+self.image)
        if (self.img.width > self.img.height):
            return True
        else:
            return False

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
