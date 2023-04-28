from flask import *
import os

static_path = '/frontend/static'
boostrap_scirpt_path = static_path + '/js/bootstrap'
jquery_scirpt_path = static_path + '/js/jquery'

index_blueprint = Blueprint('index', __name__, template_folder="../templates")


@index_blueprint.route("/")
def index():
    boostrap_js = [boostrap_scirpt_path + '/' + val for val in os.listdir('.' + boostrap_scirpt_path)]
    jquery_js = [jquery_scirpt_path + '/' + val for val in os.listdir('.' + jquery_scirpt_path)]
    return render_template("index.html", boostrap_js=boostrap_js, jquery_js=jquery_js)
