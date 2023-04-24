from flask import *

index_blueprint = Blueprint('index', __name__, template_folder="../templates")


@index_blueprint.route("/")
def index():
    return render_template("index.html")