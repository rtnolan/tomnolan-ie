from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from app.models import User, Category
from app.extensions import db
from flask import current_app, flash


class PostForm(FlaskForm):
	title = StringField("Title", validators=[Required()])
	categories = SelectMultipleField("Categories:")
	image_url = StringField("Image URL")
	body = PageDownField("What's on your mind?", validators=[Required()])
	submit = SubmitField('Submit')

	def __init__(self, choices):
		FlaskForm.__init__(self)
		self.categories.choices = choices


class AddCategoryForm(FlaskForm):
	name = StringField("Category Name:", validators=[Required()])
	submit = SubmitField("Add")