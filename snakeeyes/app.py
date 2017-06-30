from flask import Flask
from snakeeyes.blueprints.main import main

def create_app():
	"""
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
	app = Flask(__name__)
	app.config.from_object('config.settings')

	app.register_blueprint(main)

	extensions(app)

	return app


def extensions(app):
	return None