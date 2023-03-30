"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE = "https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2015/3/31/1427823466140/1fe69f2c-59d6-4e07-ab3a-8b60dbe35db2-1020x1020.jpeg?width=700&quality=85&auto=format&fit=max&s=488d904c14758c38d8010de62c742e4b"

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
	posts = db.relationship("Post", 
					cascade = "all, delete-orphan",
					backref='user')

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
	posts = db.relationship("Post", 
					secondary="posts_tags",
					cascade = "all, delete",
					backref='tags')

class PostTag(db.Model):

	__tablename__ = 'posts_tags'

	post_id = db.Column(db.Integer,
						db.ForeignKey("posts.id"),
						primary_key=True)
	tag_id = db.Column(db.Integer,
						db.ForeignKey("tags.id"),
						primary_key=True)	
	
