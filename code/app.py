from flask import *
from .backend.database.engine import *
from .backend.database.migration import *
from flask_login import *

# tra tutti i file che hanno rotte deve essere il primo in quando definisce flas_login
from .backend.src.home import *
from .backend.src.login_register import *
from .backend.src.chat import *
from .frontend.src.index import *
from .backend.src.project import *
from .backend.src.admin import *
import sys
import os

app = Flask(__name__)

app.register_blueprint(index_blueprint, url_prefix="/")
app.register_blueprint(login_register_blueprint, url_prefix="/")
app.register_blueprint(home_blueprint, url_prefix="/")
app.register_blueprint(project_blueprint, url_prefix="/")
app.register_blueprint(chat_blueprint, url_prefix="/")
app.register_blueprint(admin_blueprint, url_prefix="/")
# Secret Key for session management and flash messages
app.secret_key = os.getenv("SECRET_KEY")
migrate()  # we want to generate the db_bk table on app load

login_manager.init_app(app)
login_manager.login_view = "login_register.login"
UPLOAD_FOLDER = os.path.join(app.root_path, "db_files")
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# 5 Mb as maximum file size
app.config["MAX_CONTENT_LENGTH"] = 5 * 1000 * 1000


# login_manager = LoginManager(app)


@login_manager.user_loader
def user_loader(user_id):
    """
    Loads user from database with given ID

    @param user_id The user's ID
    @returs User associated with the ID
    """
    return get_session().query(User).filter(User.id == user_id).first()


@app.route("/favicon.ico")
def favicon():
    """
    Returns the favicon
    """
    return send_from_directory(
        os.path.join(app.root_path, "frontend", "static", "img"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/download/<file_id>")
@login_required
def download(file_id):
    from .backend.database.session import get_session
    from sqlalchemy import select
    from .backend.database.maps import project, project_files, project_history

    file_path = list(
        get_session()
        .query(ProjectFiles.path, ProjectFiles.id_project_history)
        .filter(ProjectFiles.id == file_id)
        .first()
    )

    if file_path is None:
        flash("The file does not exist.")
        return redirect(url_for("home.index"))
    # Check if user has permissions to download this file

    # TODO remove list
    project_id = list(
        get_session()
        .query(ProjectHistory.id_project)
        .filter(ProjectHistory.id == file_path[1])
        .first()
    )
    has_permission = (
        get_session()
        .query(Project)
        .filter(Project.id == project_id[0], Project.id_user == current_user.id)
        .first()
    )

    if has_permission is None:
        flash("You do not have permissions to download this file.")
        return redirect(url_for("home.index"))

    path = str(file_path[0])
    last_backslash = path.rfind("/")
    return send_from_directory(
        path[:last_backslash],
        path[last_backslash + 1 :],
        as_attachment=True,
        mimetype="application/pdf",
    )


# region socket for chat

# region workaround for library compatibility
import werkzeug
import werkzeug.serving
import werkzeug._reloader

werkzeug.serving.run_with_reloader = werkzeug._reloader.run_with_reloader
# endregion

from flask_socketio import *

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@socketio.on("message")
def handle_message(data):
    from .backend.src.chat import save_message
    from flask_login import current_user

    chat_value = request.args.get("id_project")

    # Assegna il client a uno specifico spazio dei nomi (chat)
    chat_namespace = f"/chat/{chat_value}"
    join_room(chat_namespace)

    new_message = {"user_name": current_user.name, "message": data["message"]}
    if "user has connected!" in data["message"]:
        send(new_message, room=chat_namespace)
    else:
        save_message(data["message"], current_user.id, data["id_project"])
        send(new_message, room=chat_namespace)


# endregion
if __name__ == "__main__":
    socketio.run(app, debug=True)
