from flask import Blueprint

db2 = Blueprint('db2', __name__)

from . import views
