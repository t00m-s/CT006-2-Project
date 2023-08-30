from flask_login import LoginManager, current_user, login_required
from front_project import *
from flask import Blueprint, request, jsonify, redirect, abort, flash
from ..database.session import get_session
from ..database.maps.user import User
from ..database.maps.project import Project
from ..database.maps.type import Type
from ..database.maps.project_files import ProjectFiles
from ..database.maps.project_history import ProjectHistory
from ..database.maps.state import State
from ..database.maps.role import Role
import sys
import os

from ...frontend.src.front_project import render_addproject

# Region per importare file distanti
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "src"))
# endregion
project_blueprint = Blueprint("project", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def user_loader(user_id):
    """
    Loads user from database with given ID

    @param user_id The user's ID
    @returs User associated with the ID
    """
    try:
        user = get_session().query(User).filter_by(id=user_id).first()
        get_session().commit()
    except:
        get_session().rollback()
        abort(500)  # TODO gestire benere l'errore
    return user


@project_blueprint.route("/projects")
@project_blueprint.route("/projects/<project_type>")
@login_required
def projects(project_type=None):
    """
    Route that lists all the projects
    with the given parameter

    @params project_type Type of the project
    """

    values = {}
    if project_type is not None and not project_type.isdigit():
        return "Error, value not integer"

    types = get_session().query(Type)
    projects = get_session().query(Project).filter(Project.id_user == current_user.id)
    if project_type is not None:
        types = types.filter(Type.id == project_type)
        projects = projects.filter(Project.id_user == current_user.id).filter(
            Project.id_type == project_type
        )

    types = types.all()
    projects = projects.all()
    if len(projects) == 0:
        return render_project(current_user, [])

    if len(types) == 0:
        return "Error, type not found"  # TODO 404 page

    for type in types:
        values[type.id] = {"name": type.name, "projects": []}

    for project in projects:
        values[project.id_type]["projects"].append(project)

    return render_project(current_user, values)


@project_blueprint.route("/viewproject/<project_id>", methods=["GET"])
@login_required
def viewproject(project_id):
    """
    Route that shows a single project with all previous states given the id
    as a parameter
    @params project_id ID of the project
    """
    if not project_id.isdigit():
        flash("You forgot something while creating the project.")
        return redirect("/projects")

    project = (
        get_session()
        .query(Project)
        .filter(Project.id_user == current_user.id, Project.id == project_id)
        .first()
    )

    if project is None:
        flash("Project not found")
        redirect("/projects")

    return render_viewproject(
        current_user,
        project,
    )


@project_blueprint.route("/addproject", methods=["GET", "POST"])
@login_required
def addproject():
    """
    Returns the route for addproject page
    """
    if request.method == "GET":
        return render_addproject(current_user, get_session().query(Type).all())
    elif request.method == "POST":
        try:
            get_session().begin()
            new_project = Project(
                id_user=current_user.id,
                id_type=request.form["type"],
                name=request.form["name"],
                description=request.form["description"],
            )
            get_session().add(new_project)
            get_session().commit()
        except:
            get_session().rollback()
            if not request.form["type"]:
                flash("Did you forget to select a type?")  # TODO NON FUNZIONA
            if not request.form["name"]:
                flash("Did you forget to add a name to the project?")
            if not request.form["description"]:
                flash("Did you forget to add a description to the project?")
            return "Parameters error", 500

        try:
            # You have to commit first, then you can access
            # autoincrement parameters
            # Add project history
            # 3 = Submitted for Evaluation
            new_project_history = ProjectHistory(
                id_project=new_project.id, id_state=State.getSubmittedID()
            )

            get_session().add(new_project_history)
            get_session().commit()
            # Add project files
            dir_path = os.path.join(
                os.getcwd(),
                "db_files",
                str(current_user.id),
                str(new_project.id),
                str(new_project_history.id),
            )
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        except:
            get_session().rollback()

        try:
            for file in request.files.items():
                # vogliamo solo l'oggetto della classe FileStorage non il suo key del form
                file = file[1]
                # TODO CONTROLLARE IL MIME TYPE in file.content_type
                file_path = os.path.join(dir_path, file.filename)
                file.save(file_path)
                get_session().add(
                    ProjectFiles(
                        path=file_path, id_project_history=new_project_history.id
                    )
                )
            get_session().commit()
            return jsonify({"new_project_id": new_project.id})
        except:
            # Delete directories and files
            import shutil

            shutil.rmtree(
                os.path.join(
                    os.getcwd(), "db_files", str(current_user.id), str(new_project.id)
                )
            )
            # Delete project_files commit
            get_session().rollback()
            # Delete project_history
            get_session().query(ProjectHistory).filter_by(
                id=new_project_history.id
            ).delete()
            # Delete project
            get_session().query(Project).filter_by(id=new_project.id).delete()

            get_session().commit()  # Delete does not autocommit
            return "General Error", 500


@project_blueprint.route("/vieweditableprojects", methods=["GET"])
def view_editable_projects():
    # Check if current user can review
    if not current_user.role.is_reviewer:
        flash("You do not have privileges to view this page.")
        return redirect("/projects")
    # select * from project_history
    # where id in (max_id)
    #           and id_state in (reviewable_states)
    from sqlalchemy.sql.expression import func

    sub_project_id_cur_user = (
        get_session().query(Project.id).filter(Project.id_user == current_user.id)
    )

    max_id = (
        get_session()
        .query(func.max(ProjectHistory.id))
        .filter(ProjectHistory.id_project.notin_(sub_project_id_cur_user))
        .group_by(ProjectHistory.id_project)
    )

    reviewable_states = get_session().query(State.id).filter(State.is_closed.is_(False))
    projects = (
        get_session()
        .query(ProjectHistory)
        .filter(
            ProjectHistory.id.in_(max_id),
            ProjectHistory.id_state.in_(reviewable_states),
        )
        .all()
    )

    types = get_session().query(Type.name).all()

    return render_view_editable_projects(current_user, projects, types)


@project_blueprint.route("/editproject/<project_id_state>", methods=["GET", "POST"])
@login_required
def editproject(project_id_state):
    if not project_id_state.isdigit():
        pass

    # Check if current user can review
    can_review = (
        get_session()
        .query(Role.id)
        .filter(Role.id == current_user.id_role, Role.is_reviewer.is_(True))
        .one()
    )
    if not can_review:
        flash("You do not have privileges to view this page.")
        return redirect("/projects")

    if request.method == "GET":
        reviewable_project = (
            get_session()
            .query(ProjectHistory)
            .filter(ProjectHistory.id == project_id_state)
            .one()
        )

    else:
        pass
