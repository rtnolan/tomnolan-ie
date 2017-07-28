from flask import Blueprint

authgwy = Blueprint('authgwy', __name__, template_folder='templates')

from . import views