from flask import Blueprint
from utility import render_with_lib

admin_blueprint = Blueprint("admin", __name__, template_folder="../templtates")


def render_admin(user, users_list):
    """
    Renders the admin page

    @params user Current user logged in
    @params users_list Other users that can be edited
    """
    return render_with_lib("admin.html", users=users_list)
