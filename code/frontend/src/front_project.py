from flask import Blueprint
from html import unescape
from utility import render_with_lib

project_blueprint = Blueprint("project", __name__, template_folder="../templates")

custom_javascript_edit_add = [
    "https://unpkg.com/dropzone@5/dist/min/dropzone.min.js",
    "https://cdn.tiny.cloud/1/cp187ge3odryin5mbbhjjq6vwjr3snwgc8zgakf0oql3z1yl/tinymce/6/tinymce.min.js",
    "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js",
    "/frontend/static/js/upload.js"]
custom_css_edit_add = [
    "https://unpkg.com/dropzone@5/dist/min/dropzone.min.css",
    "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",
    "/frontend/static/css/upload.css"]


def render_project(user, values):
    """
    Renders the project page

    @params user Current user logged in
    @params values Project types
    """
    # approved 1, submitted 2, changes 3, not approved 4
    return render_with_lib("projects.html", user=user, values=values)


def render_viewproject(user, project, ):
    """
    Renders the viewproject page

    @params user Current user logged in
    @params project_id Porject obj of the current project
    """
    css = ["/frontend/static/css/chat.css"]
    custom_js = [
        "https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js",
        "/frontend/static/js/chat.js",
        "/frontend/static/js/project.js",
    ]

    return render_with_lib(
        "viewproject.html",
        user=user,
        project=project,
        custom_javascript=custom_js,
        custom_css=css,
    )


def render_addproject(user, types):
    """
    Renders the addproject pages

    @params user Current user logged in
    @params types Types of possible project
    """
    return render_with_lib(
        "addproject.html",
        user=user,
        types=types,
        is_add=True,
        custom_javascript=custom_javascript_edit_add,
        custom_css=custom_css_edit_add,
    )


def render_view_editable_projects(user, projects_h, types):
    """
    Renders the vieweditableprojects page

    @params user Current user logged in
    @params projects All available editable project histories
    @params types Types of possible project
    """
    from collections import defaultdict

    filtered_projects = defaultdict(list)

    for p in projects_h:
        filtered_projects[p.project.type.name].append(p.project)
    return render_with_lib(
        "vieweditableprojects.html", user=user, projects=filtered_projects, types=types
    )


def render_editproject(user, project, states):
    """
    Renders the editproject page

    @params user Current user logged in
    @params project Project that will be reviewed
    """

    return render_with_lib("addproject.html",
                           user=user,
                           project=project,
                           is_add=False,
                           action='editproject',
                           states=states,
                           custom_javascript=custom_javascript_edit_add,
                           custom_css=custom_css_edit_add,
                           )
