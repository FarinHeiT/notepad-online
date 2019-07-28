from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from models import User


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=('GET', 'POST'))
def login():
	
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		# Retrieve  user obj from DB, if doesn't exist - it equals to None
		user = User.query.filter(User.username==username).first()

		# If wrong username or pwd -> flash error msg
		if not user or user.password != password:
			flash('Incorrect Username or Password. Please try again.')
		else:
			return redirect(url_for('index'))

	# If GET request - just render template
	return render_template('login.html')
