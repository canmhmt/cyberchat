from flask import Flask
from flask_login import LoginManager
from .routes import routing
from .models import login_manager_func
import os
import secrets


def create_app():
    app = Flask(__name__)
    app.secret_key = secrets.token_hex(32)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.config["FILE_PATH"] = f"{os.getcwd()}/templates/uploads"
    print(app.config["FILE_PATH"])
    

    login_manager_func(login_manager)
    routing(app)

    
    return app