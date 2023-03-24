"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
	db.app = app
	db.init_app(app)

class User(db.Model):
	"""USER"""
	__tablename__ = 'users'

	def __repr__(self):
		p = self
		return f"<User {p.id} {p.first_name} {p.last_name}>"

	id = db.Column(db.Integer,
					primary_key = True,
					autoincrement = True)
	first_name = db.Column(db.String,
					nullable = False)
	last_name = db.Column(db.String,
					nullable = False)
	image_url = db.Column(db.String)