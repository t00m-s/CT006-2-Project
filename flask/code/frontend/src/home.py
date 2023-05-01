from flask import *

home_blueprint = Blueprint('home', __name__, template_folder="../templates")


@home_blueprint.route('/home')  # TODO proteggere la rotta con obbligo di login
def home():
    return render_template('home.html')
