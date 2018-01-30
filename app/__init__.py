import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, current_app
from app.extensions import (
	bootstrap,
	moment,
	db,
	login_manager,
	mail,
	pagedown,
	#celery,
	#debug_toolbar,
)
from config import config

def create_app(config_name):
	"""
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
	app = Flask(__name__)
	#app.config.from_object('config.settings')
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	from app.blueprints.main import main as main_bp
	app.register_blueprint(main_bp)

	from app.blueprints.auth import auth as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	extensions(app)

	if app.config['SSL_REDIRECT']:
		from flask_sslify import SSLify
		sslify = SSLify(app)

	if not app.debug and not app.testing:
		if app.config['MAIL_SERVER']:
			auth = None
			if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
				auth = (app.config['MAIL_USERNAME'],
					app.config['MAIL_PASSWORD'])
			secure = None
			if app.config['MAIL_USE_TLS']:
				secure = ()
				mail_handler = SMTPHandler(
					mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
					fromaddr='no-reply@' + app.config['MAIL_SERVER'],
					toaddrs=app.config['MAIL_USERNAME'], subject='Blog Failure',
					credentials=auth, secure=secure)
			mail_handler.setLevel(logging.ERROR)
			app.logger.addHandler(mail_handler)

		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/microblog.log',
			maxBytes=10240, backupCount=10)
		file_handler.setFormatter(logging.Formatter(
			'%(asctime)s %(levelname)s: %(message)s '
			'[in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)

		app.logger.setLevel(logging.INFO)
		app.logger.info('Microblog startup')

	return app


def extensions(app):
	# initializes all currently used extensions in the application.
	bootstrap.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	pagedown.init_app(app)
	#celery.conf.update(app.config)
	#debug_toolbar.init_app(app)

	return None