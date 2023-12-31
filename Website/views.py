from flask import Blueprint, render_template, request, flash, jsonify, current_app, send_from_directory, url_for
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from . import db
from .models import Note, User
import json
import datetime

views = Blueprint('views', __name__)

photos = UploadSet('photos', IMAGES)  # Create an UploadSet for photo files

@views.route('/my-posts', methods=['GET', 'POST'])
@login_required
def home():
    form_identifier = request.form.get('formIdentifier')
    if request.method == 'POST' and form_identifier=='note_post':
        note = request.form.get('note')
        title = request.form.get('title')
        image = request.files.get('image')
        visibility = int(request.form.get('visibility'))

        configure_uploads(current_app, photos)

        current_date_time = datetime.datetime.now()

        if len(note) < 1:
            flash('Note is too short!', category='error')
            filename = None
        elif len(title) < 1:
            flash('Title is too short!', category='error')
            filename = None
        elif len(title) > 40:
            flash('Title is too long!', category='error')
            filename = None
        elif image and image.filename != '':
            filename = photos.save(image)
            new_note = Note(data=note, image=filename, title=title, user_id=current_user.id, visibility=visibility, date=current_date_time)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        else:
            filename = None
            new_note = Note(data=note, image=filename, title=title, user_id=current_user.id, visibility=visibility, date=current_date_time)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    if request.method == 'POST' and form_identifier == 'profile_photo_change':
        image = request.files.get('newProfileImage')
        configure_uploads(current_app, photos)

        filename = photos.save(image)
        current_user.profile_photo = filename
        db.session.commit()
        flash('Profile Photo Successfully Changed!', category='success')

    user = User.query.get(current_user.id)
    allUsers = User.query.all()
    reversed_notes = list(reversed(user.notes))
    return render_template("home.html", user=current_user, reversed_notes=reversed_notes, allUsers=allUsers)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})