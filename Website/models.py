from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz
from io import BytesIO
from PIL import Image, ExifTags


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1500))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('America/New_York')))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(100))
    title = db.Column(db.String(40))

    visibility = db.Column(db.Integer)
    presentInSearch = True

    @property
    def dateParsed(self):
        messydate = str(self.date)
        year = messydate[:4]
        month = messydate[5:7]
        if month == "01":
            month = 'January'
        elif month == '02':
            month = 'February'
        elif month == '03':
            month = 'March'
        elif month == '04':
            month = 'April'
        elif month == '05':
            month = "May"
        elif month == "06":
            month = "June"
        elif month == '07':
            month = 'July'
        elif month == '08':
            month = 'August'
        elif month == '09':
            month = 'September'
        elif month == '10':
            month = 'October'
        elif month == '11':
            month = 'November'
        elif month == '12':
            month = 'December'

        day = messydate[8:10]
        if day[1] == '1' and day[0] != '1':
            day += "st"
        elif day[1] == '2' and day[0] != '1':
            day += 'nd'
        elif day[1] == '3' and day[0] != '1':
            day += 'rd'
        else:
            day += 'th'

        time = messydate[11:16]
        if int(time[:2]) > 12:
            time = str(int(time[:2]) - 12) + time[2:]
            time += 'pm'
        elif time[:2] == '12':
            time += 'pm'
        else:
            if int(time[:2]) < 10:
                time = time[1:]
            time += 'am'

        return month + " " + day + ", " + year + ", at " + time

    @property
    def noteLength(self):
        length = len(self.data)
        if (len(self.data) > 200): length = length/1.68
        elif (len(self.data) > 390): length = length / 1.66 + 10
        else: length = length/1.8
        return length + 180

    @property
    def titleLength(self):
        length = len(self.title)
        return length

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
