from pip._vendor.rich import print
from flask import Blueprint, abort
from flask_login import LoginManager, current_user, login_required

from ..database.maps.project import Project
from ..database.maps.user import User
from ...frontend.src.front_chat import render_chat
from ..database.session import get_session
from ..database.maps.chat import Chat

chat_blueprint = Blueprint('chat', __name__)


@chat_blueprint.route('/chat/<project_id>')
@login_required
def chat(project_id):
    messages = None
    try:
        project = get_session().query(Project).filter_by(id=project_id).first()
        messages = project.messages

        # TODO CONTROLLARE CHE IL PROGETTO ESISTA E ALTRI CONTROLLI DI AUTORIZZAZIONI (chi sta facendo l'accesso) E SICUREZZA

        if messages is None:
            abort(500)
        elif len(messages) == 0:
            return 'No messages'
        return render_chat(messages)
    except:
        get_session().rollback()
        abort(500)


def save_message(message, id_sender, id_project):
    test_project = get_session().query(Project).filter(Project.id == id_project).first()
    if test_project is None:
        abort(400)
    test_user = get_session().query(User).filter(User.id == id_sender).first()
    if test_user is None:
        abort(400)
    if not (test_user.isReviewer() or test_project.id_user == test_user.id):
        abort(400)

    try:
        new_chat = Chat(message=message, id_user=id_sender, id_project=id_project)
        get_session().add(new_chat)
        get_session().commit()
    except:
        get_session().rollback()
