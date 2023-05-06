from flask import Blueprint
from .utility import render_with_lib
import os

index_blueprint = Blueprint('index', __name__, template_folder="../templates")

static_path = '/frontend/static'
style_css_path = static_path + '/css'


def get_static_resource(path, resource):
    if path[0] == '/':
        path = path[1::]
    if os.path.exists(path + '/' + resource):

        return open('./' + path + '/' + resource, 'r').read()
    else:
        return 'error'


@index_blueprint.route(style_css_path + '/<resource>')
def style_css(resource):
    return get_static_resource(style_css_path, resource)


@index_blueprint.route("/")
def index():
    return render_with_lib("index.html")
