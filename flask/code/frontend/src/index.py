from flask import *
import os

index_blueprint = Blueprint('index', __name__, template_folder="../templates")

static_path = '/frontend/static'
boostrap_script_path = static_path + '/js/bootstrap'
boostrap_css_path = static_path + '/css/bootstrap'
jquery_script_path = static_path + '/js/jquery'


def get_static_resource(path, resource):
    if path[0] == '/':
        path = path[1::]
    if os.path.exists(path + '/' + resource):
        return open('./' + path + '/' + resource).read()
    else:
        return 'error'


@index_blueprint.route("/")
def index():
    boostrap_js = [boostrap_script_path + '/' + val for val in os.listdir('.' + boostrap_script_path)]
    boostrap_css = [boostrap_css_path + '/' + val for val in os.listdir('.' + boostrap_css_path)]
    jquery_js = [jquery_script_path + '/' + val for val in os.listdir('.' + jquery_script_path)]
    return render_template("index.html", boostrap_js=boostrap_js, jquery_js=jquery_js, boostrap_css=boostrap_css)


@index_blueprint.route(boostrap_script_path + '/<resource>')
def boostrap_script(resource):
    return get_static_resource(boostrap_script_path, resource)


@index_blueprint.route(jquery_script_path + '/<resource>')
def jquery_script(resource):
    return get_static_resource(jquery_script_path, resource)


@index_blueprint.route(boostrap_css_path + '/<resource>')
def boostrap_styles(resource):
    return get_static_resource(boostrap_css_path, resource)
