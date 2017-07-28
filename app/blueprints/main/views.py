from flask import render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from . import main
from .forms import PostForm
from app.models import Post, Category
from app.extensions import db

@main.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if current_user.is_authenticated and current_user.confirmed \
	and form.validate_on_submit():
		category = Category.query.filter_by(name=form.category.data).first()
		if category is None:
			category = Category(name=form.category.data)
		post = Post(body=form.body.data, author=current_user._get_current_object())
		post.categories.append(category)
		db.session.add(post)
		return redirect(url_for('main.index'))
	return render_template('main/index.html', form=form)

@main.route('/get-category', methods=['GET', 'POST'])
@login_required
def get_category():
    return jsonify({'category': [category.name for category in Category.query.order_by(Category.name).all()]})