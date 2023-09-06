from flask import Blueprint
from utility import render_with_lib

admin_blueprint = Blueprint("admin", __name__, template_folder="../templtates")


def render_admin(user, users_list):
    """
    Renders the admin page

    @params user Current user logged in
    @params users_list Other users that can be edited
    """
    custom_javscript = [
        "/frontend/static/js/admin.js",
        "https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js",
        "https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js",
    ]
    custom_css = ["https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css"]
    return render_with_lib(
        "admin.html",
        users=users_list,
        custom_javascript=custom_javscript,
        custom_css=custom_css,
    )
