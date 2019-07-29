from flask import Blueprint
from flask_login import login_required

textEntries = Blueprint('textEntries', __name__, template_folder='templates')


@textEntries.route('/my-notes')
@login_required
def my_notes():
    return 'OK'

