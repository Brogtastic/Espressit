from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/browse', methods=['GET', 'POST'])
def browse():
    allUsers = User.query.all()
    allNotes = Note.query.all()

    sorting = 1
    search_filter = 1
    search = ""

    sorted_notes = sorted(allNotes, key=lambda note: (note.date, allNotes.index(note)), reverse=True)

    if request.method == 'POST':
        sorting = int(request.form.get('sorting'))
        if sorting == 1:
            # Sort by newest
            sorted_notes = sorted(allNotes, key=lambda note: (note.date, allNotes.index(note)), reverse=True)
        elif sorting == 2:
            # Sort by oldest
            sorted_notes = sorted(allNotes, key=lambda note: (note.date, allNotes.index(note)), reverse=False)

        search_button = request.form.get('search_button')
        if search_button == 'clicked':
            search = request.form.get('search')
            print("Search: " + search)
            search_filter = request.form.get('filter')

            #Search Titles
            if search_filter == '1':
                for note in allNotes:
                    if search.lower() in note.title.lower():
                        note.presentInSearch = True
                    else:
                        note.presentInSearch = False

            #Search Content
            if search_filter == '2':
                for note in allNotes:
                    if search.lower() in note.data.lower():
                        note.presentInSearch = True
                    else:
                        note.presentInSearch = False

            #Search Users
            if search_filter == '3':
                for note in allNotes:
                    myuser = get_user_by_id(note.user_id)
                    if search.lower() in myuser.first_name.lower():
                        note.presentInSearch = True
                    else:
                        note.presentInSearch = False

    return render_template("browse.html", allUsers=allUsers, user=current_user, sorted_notes=sorted_notes, sorting=sorting, search_filter=search_filter, search=search)





@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            default_photo = "blank-profile-picture.jpg"
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), profile_photo=default_photo)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/', methods=['GET', 'POST'])
def redirect_to_browse():
    return redirect(url_for('auth.browse'))


@auth.route('/<username>')
def user_profile(username):
    user = User.query.filter_by(first_name=username).first()  # Fetch user based on username
    allUsers = User.query.all()
    reversed_notes = list(reversed(user.notes))
    return render_template('profile.html', username=username, myuser=user, user=current_user, reversed_notes=reversed_notes, allUsers=allUsers)