from flask import render_template
from app import app

@app.route('/a')
def index():
	return 'it works!'