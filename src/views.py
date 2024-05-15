from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User, Files
from . import db

routes = Blueprint("views", __name__)
login_manager = LoginManager()
login_manager.login_view = 'index'

def initialize_login(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@routes.route("/")
@login_required
def index():
    return render_template("index.html", name=current_user.name)

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("passwd")
        
        print(f"email = {email}, passwd = {password}")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("logged in")
                return redirect(url_for("index"), code=302)

            else:
                flash("incorrect password")
        else:
            flash("you need to signup first")
        
    return render_template("login.html")

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