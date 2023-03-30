"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User, Post, Tag, PostTag, DEFAULT_IMAGE
import pdb

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
db.create_all()

# from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)

@app.route('/')
def redirect_to_users():
	return redirect('/users')


#######################  USER ROUTES  #########################

@app.route('/users')
def show_users():
	users = User.query.all()
	return render_template('users.html', users=users)

@app.route('/users/new')
def show_new_user_form():
	return render_template('user-new.html')

@app.route('/users/new', methods=['POST'])
def add_user():
	user = User(first_name = request.form['first_name'],
	last_name = request.form['last_name'],
	image_url = request.form['image_url'] or None)

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
	return render_template('user-info.html', user=user, posts=user_posts)

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
	user = User.query.get_or_404(user_id)
	return render_template('user-edit.html', user=user)

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
	user = User.query.get(user_id)
	db.session.delete(user)
	db.session.commit()
	return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
	user = User.query.get(user_id)
	tags = Tag.query.all()
	return render_template('post-add.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
	title = request.form['title']
	content = request.form['post-content']
	tag_ids = request.form.getlist('tag_ids')

	post = Post(title=title, content=content, author_id=user_id)
	db.session.add(post)
	db.session.commit()

	for id in tag_ids:
		post_tag = PostTag(post_id=post.id, tag_id=id)
		db.session.add(post_tag)
	db.session.commit()

	return redirect(f"/users/{user_id}")



#######################  POSTS ROUTES  ###########################

@app.route('/posts/<int:post_id>')
def show_post(post_id):
	post = Post.query.get(post_id)
	user = User.query.get(post.author_id)
	tags = Tag.query.all()

	return render_template('post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	tags = Tag.query.all()

	return render_template('post-edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
	post = Post.query.get_or_404(post_id)
	tag_ids = [int(id) for id in request.form.getlist('tag_ids')]

	post.title = request.form['title']
	post.content = request.form['post-content']
	post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

	db.session.commit()

	return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
	post = Post.query.get(post_id)
	db.session.delete(post)
	db.session.commit()
	return redirect(f"/users/{post.author_id}")


#####################  TAG ROUTES  #######################

@app.route('/tags')
def show_tags():
	tags = Tag.query.all()
	return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
	return render_template('tag-add.html')

@app.route('/tags/new', methods=['POST'])
def add_new_tag():
	tag_name = request.form['tag_name']
	tag = Tag(name=tag_name)
	db.session.add(tag)
	db.session.commit()
	return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
	tag = Tag.query.get(tag_id)
	posts = tag.posts
	return render_template('tag-show.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
	tag = Tag.query.get(tag_id)
	return render_template('tag-edit.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
	tag = Tag.query.get_or_404(tag_id)

	tag.name = request.form['tag_name']

	db.session.commit()
	return redirect('/tags')

# @app.route('/tags/<int:tag_id>/delete', methods=['POST'])
# def delete_tag(tag_id):
