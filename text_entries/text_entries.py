from flask import Blueprint, render_template, request, flash, abort
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import TextEntry
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
    notes = TextEntry.query.filter(TextEntry.author_id==current_user.id).all()
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
            except:
                flash('Something went wrong.')


    expires_date = str(datetime.today() + timedelta(days=1))
    return render_template('create_note.html', expires_date=expires_date)


@textEntries.route('/my-notes/<link>', methods=('GET', 'POST'))
@login_required
def note_detail(link):

    note = TextEntry.query.filter(TextEntry.link==link).first()

    if note.publicity == 0 and current_user.id != note.author_id:
        abort(403)
        
    if request.method == 'POST':
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
    
    return render_template('note_detail.html', note=note)