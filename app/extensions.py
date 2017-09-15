from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
#from flask_debugtoolbar import DebugToolbarExtension
#from celery import Celery
from config import Config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown = PageDown()
#debug_toolbar = DebugToolbarExtension()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'authgwy.login'


# Initialize Celery
#celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)