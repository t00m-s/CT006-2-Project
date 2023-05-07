from flask import *
from utility import *

home_blueprint = Blueprint('home', __name__, template_folder="../templates")


def home(user):
    return render_with_lib('home.html', user)
