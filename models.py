from app import db
from datetime import datetime


starred_entry = db.Table('starred_entry', 
						 db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
						 db.Column('entry_id', db.Integer, db.ForeignKey('text_entry.id'))
						 )

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(100))
	secret_q = db.Column(db.String(255))
	secret_q_ans = db.Column(db.String(255))

	starred_entries = db.relationship('TextEntry', secondary=starred_entry, backref=db.backref('starred_by'), lazy='dynamic')

	def __repr__(self):
		return f'<Username: {self.username}. User id {self.id}>'

class TextEntry(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author_id = db.ForeignKey('user.id')
	body = db.Column(db.Text(2555))
	name = db.Column(db.String(255))
	created_date = db.Column(db.DateTime, default=datetime.now())
	link = db.Column(db.String(155), unique=True)
	publicity = db.Column(db.Boolean())
	expires_on = db.Column(db.DateTime)
