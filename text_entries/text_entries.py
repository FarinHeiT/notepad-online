from flask import Blueprint, render_template, request, flash, abort, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import TextEntry, User
from app import db
import hashlib


textEntries = Blueprint('textEntries', __name__, template_folder='templates')


def generateLink(name):
    ''' Creates hash link based on the name and current datetime '''
    link = hashlib.md5()
    link.update(name.encode('utf-8') + str(datetime.now()).encode('utf-8'))
    return link.hexdigest()[:10]

@textEntries.route('/my-notes')
@login_required
def my_notes():
    ''' Return notes created by current user and that aren't expired '''

    # Delete expired Notes
    try:
        expired_notes = TextEntry.query.filter(TextEntry.expires_on < datetime.today()).delete()
        db.session.commit()
    except:
        print(f'Something went wrong. Tried to delete expired notes.')

    # Get current page argument (if not specified - then first page)
    page = int(request.args.get('page')) if request.args.get('page') and request.args.get('page').isdigit() else 1

    if 'starred' in request.args:
        # Get current user
        user = User.query.filter(User.id==current_user.id).first()
        # Get starred notes of the current user
        notes = user.starred_entries.paginate(page, 6)

    else:
        # Get all notes for current page
        notes = TextEntry.query.filter(TextEntry.author_id==current_user.id,
                                    TextEntry.expires_on > datetime.today()).paginate(page, 6)

    return render_template('my_notes.html', notes=notes)


@textEntries.route('/my-notes/create', methods=('GET', 'POST'))
@login_required
def create_note():

    if request.method == 'POST':
        name = request.form.get('name')
        body = request.form.get('body')
        private = bool(request.form.get('private'))
        expires_on = datetime.strptime(request.form.get('expires'), '%Y-%m-%d')
        author_id = current_user.id
        link = generateLink(name)

        if not name or len(name) < 10:
            flash('Name must be specified.')
        elif not body or len(body) < 10:
            flash('Body must be specified.')
        else:
            try:
                note = TextEntry(name=name, body=body,
                                link=link, publicity=private,
                                author_id=author_id, expires_on=expires_on)
                db.session.add(note)
                db.session.commit()

                return redirect(url_for('textEntries.note_detail', link=link))

            except:
                flash('Something went wrong.')


    expires_date = str(datetime.today() + timedelta(days=1))
    return render_template('create_note.html', expires_date=expires_date)


@textEntries.route('/my-notes/<link>', methods=('GET', 'POST'))
@login_required
def note_detail(link):

    try:
        note = TextEntry.query.filter(TextEntry.link==link).first()
        # Determine whether note is already starred by current user
        starred = bool(list(filter(lambda x: x.id == current_user.id, note.starred_by)))
        if note == None:
            flash('No such note.')
            return redirect(url_for('index'))
    except:
        print('Something went wrong. Tried to get specified note.')

    if note.publicity == 1 and current_user.id != note.author_id:
        abort(403)
        
    if request.method == 'POST' and note.author_id == current_user.id:
        note.name = request.form.get('name')
        note.body = request.form.get('body')
        note.publicity = bool(request.form.get('private'))
        note.expires_on = datetime.strptime(request.form.get('expires'), '%Y-%m-%d')

        if not note.name or len(note.name) < 10:
            flash('Name must be specified.')
        elif not note.body or len(note.body) < 10:
            flash('Body must be specified.')
        else:
            try:
                db.session.add(note)
                db.session.commit()
            except:
                flash('Something went wrong.')
    
    return render_template('note_detail.html', note=note, starred=starred)


@textEntries.route('/_star-note')
def star_note():

    data = {
        'status': 'success'
    }

    note_id = request.args.get('note_id')
    author_id = request.args.get('author_id')

    note = TextEntry.query.filter(TextEntry.id==note_id).first()
    if request.args.get('action') == 'star':
        # If already starred then show err
        if list(filter(lambda x: x.id == int(author_id), note.starred_by)):
            data['result'] = 'error'
        else:
            data['result'] = 'success'
            note.starred_by.append(
                User.query.filter(User.id==author_id).first()
            )
            db.session.commit()
    else:
        data['result'] = 'success'
        note.starred_by.remove(
            User.query.filter(User.id==author_id).first()
        )
        db.session.commit()

    return jsonify(data)