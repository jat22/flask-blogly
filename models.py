"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 
import datetime

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
	# post = db.relationship('Post', backref='users')

class Post(db.Model):
	"""POST"""
	__tablename__ = 'posts'

	def __rep__(self):
		p = self
		return f"<Post {p.id} {p.title} {p.created_at} {p.author_id}>"

	id = db.Column(db.Integer,
					primary_key = True,
					autoincrement = True)
	title = db.Column(db.String,
					nullable = False)
	content = db.Column(db.String)
	created_at =  db.Column(db.DateTime, 
					nullable=False, 
					default=datetime.datetime.now())
	author_id = db.Column(db.Integer,
					db.ForeignKey('users.id'))