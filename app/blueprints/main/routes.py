from flask import render_template, redirect, url_for, jsonify, json, request, flash, abort, current_app
from flask_login import current_user, login_required
from . import main
from ...decorators import admin_required
from .forms import PostForm, AddCategoryForm
from app.models import Post, Category
from app.extensions import db
from flask_sqlalchemy import get_debug_queries

@main.after_app_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
			current_app.logger.warning('Slow query: %s\nParameters: %s\nDuration: %f\nContext %s\n' %
										(query.statement, query.parameters, query.duration, query.context))

	return response

@main.route('/', methods=['GET', 'POST'])
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items
	return render_template('main/index.html', posts=posts, pagination=pagination)

@main.route('/about', methods=['GET'])
def about():
	return render_template('main/about.html')


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('main/post.html', post=post)


@main.route('/add-post', methods=['GET','POST'])
@login_required
@admin_required
def add_post():
	db_categories = Category.query
	choices = [(c.name, c.name) for c in db_categories]
	form = PostForm(choices)
	if current_user.is_authenticated and current_user.confirmed \
	and form.validate_on_submit():
		post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
		for category_str in request.form.getlist('categories'):
			category = Category.query.filter_by(name=category_str).first()
			post.categories.append(category)
			db.session.add(post)
		print(request.form.getlist('categories'))
		return redirect(url_for('main.index'))
	return render_template('main/add_post.html', form=form)


@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(id):
	post = Post.query.get_or_404(id)
	db_categories = Category.query
	choices = [(str(c.id), c.name) for c in db_categories]
	if current_user != post.author:
		abort(403)
	form = PostForm(choices)
	if current_user.is_authenticated and current_user.confirmed \
	and form.validate_on_submit():
		post.title = form.title.data
		post.body = form.body.data
		post.categories = []
		for category_str in request.form.getlist('categories'):
			category = Category.query.filter_by(id=category_str).first()
			post.categories.append(category)
			db.session.add(post)
		flash('Post has been updated.')
		return redirect(url_for('main.post', id=id))
	form.title.data = post.title
	form.body.data = post.body
	form.categories.default = [ (str(category.id)) for category in post.categories ]
	form.categories.process(request.form)
	return render_template('main/edit_post.html', form=form, id=id)

@main.route('/delete-post/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_post(id):
	post = Post.query.get_or_404(id)
	db.session.delete(post)
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items

	return render_template('main/index.html', posts=posts, pagination=pagination)


@main.route('/add-category', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
	form = AddCategoryForm()
	if current_user.is_authenticated and current_user.confirmed \
	and form.validate_on_submit():
		category = Category.query.filter_by(name=form.name.data).first()
		if category is None:
			category = Category(name=form.name.data)
			db.session.add(category)
			return redirect(url_for('main.add_post'))
		flash("Category already exists.")
	return render_template('main/add_category.html', form=form)


@main.route('/add-category/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_add_category(id):
	post = Post.query.get_or_404(id)
	form = AddCategoryForm()
	db_categories = Category.query
	choices = [(c.name, c.name) for c in db_categories]
	pform = PostForm(choices)
	if current_user.is_authenticated and current_user.confirmed \
	and form.validate_on_submit():
		category = Category.query.filter_by(name=form.name.data).first()
		if category is None:
			category = Category(name=form.name.data)
			db.session.add(category)
			return redirect(url_for('main.edit_post', id=id))
		flash("Category already exists.")
	return render_template('main/edit_add_category.html', form=form, id=id)

@main.route('/delete-category/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_category(id):

	page = request.args.get('page', 1, type=int)

	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)

	posts = pagination.items
	category = Category.query.filter_by(id=id).first()
	db.session.delete(category)

	return render_template('main/index.html', posts=posts, pagination=pagination)














