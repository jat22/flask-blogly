"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE = "https://media.istockphoto.com/id/1316420668/vector/user-icon-human-person-symbol-social-profile-icon-avatar-login-sign-web-user-symbol.jpg?s=612x612&w=0&k=20&c=AhqW2ssX8EeI2IYFm6-ASQ7rfeBWfrFFV4E87SaFhJE="

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
	image_url = db.Column(db.String, 
					nullable=False,
					default = DEFAULT_IMAGE)
	post = db.relationship('Post', backref='user', 
					cascade = 'all, delete-orphan')

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
	tag = db.relationship('Tag', 
					secondary='posts_tags', 
					backref='posts')

class Tag(db.Model):
	"""TAG"""

	__tablename__ = "tags"

	def __ref__(self):
		return f"<Tag {self.name} >"

	id = db.Column(db.Integer,
					primary_key = True,
					autoincrement = True)
	name = db.Column(db.Text,
					unique = True)

class PostTag(db.Model):

	__tablename__ = 'posts_tags'

	post_id = db.Column(db.Integer,
						db.ForeignKey("posts.id"),
						primary_key=True)
	tag_id = db.Column(db.Integer,
						db.ForeignKey("tags.id"),
						primary_key=True)	
	
