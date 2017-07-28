from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from app.models import User, Category
from app.extensions import db
from flask import current_app


#app = current_app

#db.init_app(app)

#def get_all_categories():      
#    return db.session.query(Category).all()

class PostForm(FlaskForm):
	body = PageDownField("What's on your mind?", validators=[Required()])
	#category = SelectField('Category', coerce=int)
	submit = SubmitField('Submit')
	skill_level = QuerySelectField(u'Category', query_factory=lambda: Category.query, get_label='name')