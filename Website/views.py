from flask import Blueprint, render_template, request, flash, jsonify, current_app, send_from_directory, url_for
from flask_login import login_required, current_user
from flask_uploads import UploadSet, IMAGES, configure_uploads
from . import db
from .models import Note
import json
from Website import create_app
from os import path

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        image = request.files.get('image')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        elif image:
            photos = current_app.config['UPLOADED_PHOTOS_DEST']
            filename = photos.save(image)
            new_note = Note(data=note, image=filename, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        else:
            filename = None
            new_note = Note(data=note, image=filename, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

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