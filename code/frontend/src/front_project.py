from flask import Blueprint
from html import unescape
from utility import render_with_lib

project_blueprint = Blueprint(
    'project', __name__, template_folder="../templates")


def render_project(user, values):
    '''
    Renders the project page

    @params user Current user logged in
    @params values Project types
    '''
    # approved 1, submitted 2, changes 3, not approved 4
    return render_with_lib('projects.html', user=user, values=values)


def render_viewproject(project, project_histories, files):
    '''
    Renders the viewproject page

    @params user Current user logged in
    @params project_id ID of the current project
    @params history_id ID of the state of the current project
    @params files Saved files on the current history
    '''
    css = ['/frontend/static/css/chat.css']
    custom_js = ['https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js',
                 '/frontend/static/js/chat.js',
                 '/frontend/static/js/project.js']

    # filtered_project = list(project)

    from collections import defaultdict
    grouped_files = defaultdict(list)
    for file in files:
        grouped_files[file.history_id].append(file)

    return render_with_lib('viewproject.html', project=project,
                           project_histories=project_histories,
                           files=grouped_files, custom_javascript=custom_js, custom_css=css)


def render_addproject(user, types):
    '''
    Renders the addproject pages

    @params user Current user logged in
    @params types Types of possible project
    '''
    custom_javascript = ['https://unpkg.com/dropzone@5/dist/min/dropzone.min.js',
                         'https://cdn.tiny.cloud/1/cp187ge3odryin5mbbhjjq6vwjr3snwgc8zgakf0oql3z1yl/tinymce/6/tinymce.min.js',
                         'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
                         '/frontend/static/js/upload.js']
    custom_css = ['https://unpkg.com/dropzone@5/dist/min/dropzone.min.css',
                  'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css',
                  '/frontend/static/css/upload.css']

    return render_with_lib('addproject.html', user=user, types=types,
                           custom_javascript=custom_javascript,
                           custom_css=custom_css)
