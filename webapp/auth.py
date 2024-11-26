from flask import Blueprint, redirect, render_template, request, session, url_for

# NOTE: change these env vars!
env_username = 'defaultUser'
env_password = 'defaultPassword'

auth = Blueprint('auth', __name__)

# checks if session cookie matches account
# use in ternary form like:
# return render_template("template.html") if authorized() else redirect(url_for('auth.login'))
# if logged in, go where you expect; else, redirect to login page
def authorized():
    try: return ((session["username"] == env_username) and (session["password"] == env_password))
    except: return False

# redirect to login
@auth.route('/')
def authRoot():
    return redirect(url_for('auth.login'))

# creates a session cookie
@auth.route('/login/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
    return redirect(url_for('views.homeView')) if authorized() else render_template("login.html")

# clears the session cookie
@auth.route('/logout/')
def logout():
    session["username"] = None
    session["password"] = None
    return redirect(url_for('views.homeView'))
