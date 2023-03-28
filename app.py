"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post
import pdb


app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route('/')
def redirect_to_users():
	return redirect('/users')

@app.route('/users')
def show_users():
	users = User.query.all()
	return render_template('users.html', users=users)

@app.route('/users/new')
def show_new_user_form():
	return render_template('new-user-form.html')

@app.route('/users/new', methods=['POST'])
def add_user():
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	image_url = request.form['image_url']

	user = User(first_name=first_name, last_name=last_name, image_url=image_url)
	db.session.add(user)
	db.session.commit()

	return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
	user = User.query.get_or_404(user_id)
	posts = Post.query.all()
	user_posts = []
	for post in posts:
		if post.author_id == user.id:
			user_posts.append(post)
	return render_template('user_info.html', user=user, posts=user_posts)

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
	user = User.query.get_or_404(user_id)
	
	user.first_name = request.form['first_name']
	user.last_name = request.form['last_name']
	user.image_url = request.form['image_url']

	db.session.commit()

	return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
	User.query.filter_by(id=user_id).delete()
	db.session.commit()
	return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
	user = User.query.get(user_id)
	return render_template('add-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
	title = request.form['title']
	content = request.form['post-content']

	post = Post(title=title, content=content, author_id=user_id)
	db.session.add(post)
	db.session.commit()

	return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
	post = Post.query.get(post_id)
	user = User.query.get(post.author_id)
	return render_template('post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	print(post)
	return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	user_id = post.author_id

	post.title = request.form['title']
	post.content = request.form['post-content']

	db.session.commit()

	return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	post = Post.query.get(post_id)
	user_id = post.author_id
	Post.query.filter_by(id=post_id).delete()
	db.session.commit()
	return redirect(f"/users/{user_id}")