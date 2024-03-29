from flask import Blueprint, send_file, abort
from .utility import render_with_lib
import os

index_blueprint = Blueprint('index', __name__, template_folder="../templates")

static_path = '/frontend/static'
style_css_path = static_path + '/css'
img_path = static_path + '/img'
script_js_path = static_path + '/js'


def get_static_resource(path, resource, extention):
    if path[0] == '/':
        path = path[1::]
    if os.path.exists(path + '/' + resource):
        mime = 'text/html'
        if extention == 'css':
            mime = 'text/' + extention
        elif extention == 'js':
            mime = 'application/javascript'
        elif extention in ['json', 'pdf', 'xml']:
            mime = 'application/' + extention
        elif extention in ['png', 'img', 'jpeg', 'gif', 'svg', 'webp']:
            mime = 'image/' + extention
        else:
            abort(500)
        return send_file('./' + path + '/' + resource, mimetype=mime)
    else:
        return abort(404)


@index_blueprint.route(style_css_path + '/<resource>')
def style_css(resource):
    return get_static_resource(style_css_path, resource, 'css')


@index_blueprint.route(img_path + '/<resource>')
def images(resource):
    return get_static_resource(img_path, resource, 'img')


@index_blueprint.route(script_js_path + '/<resource>')
def js_script(resource):
    return get_static_resource(script_js_path, resource, 'js')
