"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User
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
	return render_template('user_info.html', user=user)

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
