from unittest import TestCase
import pdb
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
	"""Test for views of Users"""

	def setUp(self):
		"""Add sample user"""

		User.query.delete()

		user = User(first_name = "First", last_name="Last", image_url="testing.com")
		db.session.add(user)
		db.session.commit()

		self.user_id = user.id
		self.user = user
		# pdb.set_trace()


	def tearDown(self):
		db.session.rollback()

	def test_show_users(self):
		with app.test_client() as client:
			resp = client.get('/users')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("<h3>USERS</h3>", html)

	def test_show_new_user_form(self):
		with app.test_client() as client:
			resp = client.get('/users/new')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn("<title>Add New User</title>", html)

	def test_show_user(self):
		with app.test_client() as client:
			resp = client.get(f"/users/{self.user_id}")
			html = resp.get_data(as_text=True)
			self.assertIn("<title>User Info</title>", html)

	def test_delete_userself(self):
		with app.test_client() as client:
			resp = client.post(f"/users/{self.user_id}/delete")
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 302)


