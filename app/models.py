from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin
from app.extensions import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin, db.Model):
	# Defines the User model that will be used.
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default=False)
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		"""
		Encrypts user password so to not store passwords in plain text.
		:param self: User object in context.
		:param password: password that is passed in from Form.
		"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		"""
		Verifies password is correct using the password hash.
		:param self: User object in context.
		:param password: password that is passed in from Form.

		:return: Boolean
		"""
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		"""
		Generates a confirmation token what will be sent as part of an email for registering a User.
		:param: self: User object.
		:param: expiration: How long before the token will expire. Defaults to 3600 seconds.

		:return: a serialized token.
		"""
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		"""
		Used to confirm the token is valid.
		:param: self: User object.
		:param: token: Token being passed in to confirm is valid.

		:return: Boolean
		"""
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False

		self.confirmed = True
		db.session.add(self)
		return True

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		return True

@login_manager.user_loader
def load_user(user_id):
	# loads User object by id (Required callback by flask_login)
    return User.query.get(int(user_id))

class Category(db.Model):
	__tablename__ = 'categories'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)

has_category = db.Table('has_category',
            db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
            db.Column('post_id', db.Integer, db.ForeignKey('posts.id')))

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	categories = db.relationship('Category', 
							secondary=has_category, 
							backref=db.backref('posts',lazy='dynamic'),
							lazy='dynamic')

























