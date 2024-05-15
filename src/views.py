from flask import Blueprint, flash, render_template, redirect, url_for, request, send_file
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User, Files
from . import db

import io

routes = Blueprint("views", __name__)
login_manager = LoginManager()
login_manager.login_view = 'views.login'

def initialize_login(app):
    login_manager.init_app(app)

def get_filenames(current_user):
    return Files.query.filter_by(user_id=current_user.id).all()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@routes.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        file_id = request.form.get("file_id")
        file = Files.query.filter_by(id=file_id).first()
        if file:
            return send_file(
                io.BytesIO(file.file_data),
                mimetype='application/pdf'
            )

        return redirect(url_for("views.index"))
    
    return render_template("index.html", name=current_user.name, files=get_filenames(current_user))

@routes.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    new_file = Files(user_id=current_user.id, filename=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()

    return redirect(url_for("views.index"))

@routes.route("/delete", methods=["POST"])
def delete():
    file_id = request.form.get("file_id")

    if file_id:
        file = db.session.get(Files, file_id)
        db.session.delete(file)
        db.session.commit()
        print(f"deleted file {request.form.get('file_id')}")

    return redirect(url_for("views.index"))

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        print(f"email = {email}, passwd = {password}")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("logged in")
                return redirect(url_for("views.index"), code=302)

            else:
                flash("incorrect password")
        else:
            flash("you need to signup first")
        
    return render_template("login.html")

@routes.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("views.login"))

@routes.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        

        print(f"name = {name}, email = {email}, passwd = {password1}, {password2}")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("email already in use")

        elif password1 != password2:
            flash("Re-Enter the same password")

        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("views.login"))


    return render_template("signup.html")
