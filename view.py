from flask import render_template, url_for, redirect
from flask_login import current_user
from app import app

@app.route('/')
def index():
	''' If the user is authenticated then redirect to my-notes, else index ''' 
	if current_user.is_authenticated:
		return redirect(url_for('textEntries.my_notes'))

	return render_template('index.html')