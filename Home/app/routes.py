from .models import querys, User, show_stock_status_query
from flask import redirect, url_for, request, abort, render_template
from flask_login import login_user, login_required, logout_user, current_user
import os
import time
from datetime import datetime


def routing(app):

    @app.route("/", methods= ["POST", "GET"])
    def login():
        if request.method == "GET":
            wrong_pass = request.args.get("wrong_pass")
            usernot_found = request.args.get("usernot_found")

            return render_template("login.html",  wrong_pass = wrong_pass, usernot_found = usernot_found)
        
        if request.method == "POST":

            name = request.form.get("usernamelogin")
            password = request.form.get("passwordlogin")

            login_query = querys.login_user_query(name)

            if login_query:
                
                if password == login_query[1]:
                    login_user(User(name=name))
                    return redirect(url_for("stocks", name = name))

                else:
                    wrong_pass = "The password is wrong."
                    return redirect(url_for("login", wrong_pass = wrong_pass))
                
            else:
                usernot_found = "The user could not found."
                return redirect(url_for("login", usernot_found = usernot_found))
        


    @app.route("/upload/<name>", methods = ["POST"])
    @login_required
    def upload(name):
        if request.method == "POST":
            file = request.files.get("file")

            epochtime = time.time()
            readable_time = datetime.fromtimestamp(epochtime)

            filename_split = file.filename.rsplit(".", 1)

            filename = f"{filename_split[0]} {readable_time}.{filename_split[1]}"

            file_path = os.path.join(app.config["FILE_PATH"], name, filename)
            file.save(file_path)

            return redirect(url_for("profile", name = name))



    @app.route("/profile/<name>")
    @login_required
    def profile(name):
        return render_template("main.html",name = name)
    

    @app.route("/stocks/<name>")
    @login_required
    def stocks(name):
        products = show_stock_status_query.show_zara_stock_status_query(name)
        
        return render_template("stocks.html", name = name, products = products)
    

    @app.route("/stocks/upload/<name>", methods = ["POST"])
    @login_required
    def stocks_upload(name):
        if request.method == "POST":
            url = request.form.get("zara_link")
            querys.zara_link_insert_query(url, name)
            return redirect(url_for("stocks", name = name))


        


    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))
    


    # @app.route("/zara_links_query/<name>")
    # def zara_urls_query(name):
    #     
        
        

    

            
