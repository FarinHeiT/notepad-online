from flask import Blueprint, render_template
from app import db


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/')
def index():
	return 'auth bp works!'