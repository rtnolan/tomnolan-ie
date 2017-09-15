from flask import Flask, current_app
from app.blueprints.main import main
from app.blueprints.authgwy import authgwy
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

	app.register_blueprint(main)
	app.register_blueprint(authgwy, url_prefix='/authgwy')

	extensions(app)

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