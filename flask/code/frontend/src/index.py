from flask import *
import os

index_blueprint = Blueprint('index', __name__, template_folder="../templates")

static_path = '/frontend/static'

"""
boostrap_script_path = static_path + '/js/bootstrap'
boostrap_css_path = static_path + '/css/bootstrap'
jquery_script_path = static_path + '/js/jquery'
"""


def get_static_resource(path, resource):
    if path[0] == '/':
        path = path[1::]
    if os.path.exists(path + '/' + resource):
        return open('./' + path + '/' + resource).read()
    else:
        return 'error'


@index_blueprint.route("/")
def index():
    boostrap_js = [
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>']
    boostrap_css = [
        '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">']
    jquery_js = [
        '<script src="https://code.jquery.com/jquery-3.6.4.min.js" integrity="sha256-oP6HI9z1XaZNBrJURtCoUT5SUnxFr8s3BzRl+cbzUq8=" crossorigin="anonymous"></script>']
    return render_template("index.html", boostrap_js=boostrap_js, jquery_js=jquery_js, boostrap_css=boostrap_css)


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
