from flask import Flask
from .routes import registeration_routing, users_route
import secrets
from flask_login import LoginManager
from .models import login_manager_func
from flask_socketio import SocketIO
from flask_mail import Mail, Message

socket = SocketIO()

def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)
    socket.init_app(app)

    mail = Mail(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    profile_picture_upload_folder = "/home/ubuntu/Desktop/CODE/PROJECTS/SocketChat/app/templates/profile_photos/"
    sended_picture_upload_folder = "/home/ubuntu/Desktop/CODE/PROJECTS/SocketChat/app/templates/sended_photos/"

    allowed_extentions = {"jpg", "png", "gif", "jpeg", "webp"}

    def allowed_files(filename):    
        return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extentions
    
    registeration_routing(app, socket, mail, Message)
    users_route(app, socket, profile_picture_upload_folder, sended_picture_upload_folder, allowed_files)

    login_manager_func(login_manager)


    return app


