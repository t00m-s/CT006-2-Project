from flask import *

home_blueprint = Blueprint('home', __name__, template_folder="../templates")


def home():
    return render_template('home.html')
