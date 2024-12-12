from flask import redirect, url_for, request, render_template, send_from_directory, abort
from .models import query, User, profile_picture_queries
from flask_login import login_user, logout_user, login_required, current_user
from flask_socketio import send
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os


def registeration_routing(app, socket, mail, Message):
        
    @app.route('/')
    def index():
        return render_template('main.html')
    


    @app.route("/sign" , methods = ["POST", "GET"])
    def sign():
        if request.method == "GET":
            return render_template("sign.html")
        
        if request.method == "POST":
            name = request.form.get("name")
            password = request.form.get("password")
            email = request.form.get("email")

            hashed_password = generate_password_hash(password)

            query.create_user_query(name, hashed_password, email)
            
            return redirect(url_for("login"))



    @app.route("/login", methods = ["POST", "GET"])
    def login():
        if request.method == "GET":
            password_wrong = request.args.get("message_password")
            usernot_found = request.args.get("messageUser")

            return render_template("login.html", wrong_pass = password_wrong, usernot_found = usernot_found)
        
        if request.method == "POST":
            namelogin = request.form.get("usernamelogin")
            passwordlogin = request.form.get("passwordlogin")

            querys = query.read_user_query(namelogin)
            if querys:
                check_pass = check_password_hash(querys[2], passwordlogin)
                if check_pass:
                    login_user(User(name = namelogin))
                    return redirect(url_for("profile", name = namelogin))
                
                message_password = "The password is wrong."
                return redirect(url_for("login", message_password = message_password))
                
            else:
                messageUser = "The user not found."
                return redirect(url_for("login", messageUser = messageUser))



            
def users_route(app, socket, profile_picture_upload_folder, sended_picture_upload_folder, allowed_files):

    @app.route("/profile/<name>")
    @login_required
    def profile(name):
        if current_user.id != name:
            return redirect(url_for("profile", name = current_user.name))
        
        user = query.read_user_query(name)

        profile_picture_url = url_for("profile_picture", name = name)
        
        return render_template("chat.html", username = name, picture_user = name)
    



    @app.route("/profile/upload_profile_picture/<name>", methods = ["POST"])
    @login_required
    def profile_picture_upload(name):
        if current_user.id != name:
            return redirect(url_for("profile", name = current_user.name))
        
        file = request.files.get("profile_picture")

        if file and allowed_files(file.filename):
            
            profile_picture_id = query.read_user_query(name)[0]
            profile_picture_exists = profile_picture_queries.read_profile_picture_path_query(profile_picture_id)
            
            if profile_picture_exists:
                profile_picture_queries.delete_profile_picture_path_query(profile_picture_id)

            filename = file.filename

            file_path = os.path.join(profile_picture_upload_folder, filename)

            user_query = query.read_user_query(name)
            profile_picture_queries.save_profile_picture_path_query(file_path, user_query[0])
            

            file.save(file_path)

            return redirect(url_for("profile", name = name))
        


    @app.route("/profile/profile_picture/<name>")
    @login_required
    def profile_picture(name):
        
        user_id = query.read_user_query(name)
        picture = profile_picture_queries.read_profile_picture_path_query(user_id[0])

        if picture:
            picture_path = picture[0]
            picture_name = picture_path.rsplit("/", 1)[1]
            

            try:
                return send_from_directory(profile_picture_upload_folder, picture_name)
            
            except FileNotFoundError:
                abort(404)



    @app.route("/logout")
    @login_required
    def logout():
        logout_user()

        return redirect(url_for("login"))
        
            

    @socket.on('message')
    def handle_message(msg):
        print(f"Received message: {msg}")

        msg = f"{current_user.id}: {msg}"

        send(msg, broadcast=True)


