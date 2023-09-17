from flask import Blueprint
from utility import render_with_lib

admin_blueprint = Blueprint("admin", __name__, template_folder="../templtates")


def render_admin(user, users_list, columns, roles):
    """
    Renders the admin page

    @params user Current user logged in
    @params users_list Other users that can be edited
    """
    custom_javascript = [
        "https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js",
        "https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js",
        "/frontend/static/js/admin.js",
    ]
    custom_css = ["https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css"]
    return render_with_lib(
        "admin.html",
        users=users_list,
        columns=columns,
        roles=roles,
        custom_javascript=custom_javascript,
        custom_css=custom_css,
    )
