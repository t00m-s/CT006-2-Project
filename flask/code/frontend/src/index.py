from flask import Blueprint
from .utility import render_with_lib
import os

index_blueprint = Blueprint('index', __name__, template_folder="../templates")

static_path = '/frontend/static'

"""
boostrap_script_path = static_path + '/js/bootstrap'
boostrap_css_path = static_path + '/css/bootstrap'
jquery_script_path = static_path + '/js/jquery'
"""

'''
def get_static_resource(path, resource):
    if path[0] == '/':
        path = path[1::]
    if os.path.exists(path + '/' + resource):
        return open('./' + path + '/' + resource).read()
    else:
        return 'error'
'''

style_css_path = static_path + '/css'

@index_blueprint.route(style_css_path + '/<resource>')
def style_css(resource):
    return get_static_resource(style_css_path, resource)

@index_blueprint.route("/")
def index():
   return render_with_lib("index.html")
"""
@index_blueprint.route(boostrap_script_path + '/<resource>')
def boostrap_script(resource):
    return get_static_resource(boostrap_script_path, resource)


@index_blueprint.route(jquery_script_path + '/<resource>')
def jquery_script(resource):
    return get_static_resource(jquery_script_path, resource)


@index_blueprint.route(boostrap_css_path + '/<resource>')
def boostrap_styles(resource):
    return get_static_resource(boostrap_css_path, resource)
"""
