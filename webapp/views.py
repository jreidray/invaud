from flask import Blueprint, render_template
import database

views = Blueprint('views', __name__)

@views.route("/")
def homePage():
    return "<h1>Homepage</h1>"

@views.route("/extras/")
def extrasView():
    DB, db = database.init()
    items = database.overFound(db)
    DB.close()
    return render_template('extra.html', items=items)

@views.route("/incomplete/")
def missingView():
    DB, db = database.init()
    items = database.underRoom(db)
    DB.close()
    return render_template('incomplete.html', items=items)

@views.route("/misplaced/")
def missingView():
    DB, db = database.init()
    items = database.wrongSpot(db)
    DB.close()
    return render_template('misplaced.html', items=items)

@views.route("/missing/")
def missingView():
    DB, db = database.init()
    items = database.notFound(db)
    DB.close()
    return render_template('missing.html', items=items)


@views.route('/room/<room>/')
def roomView(room):
    # shows the room view
    return f'User {escape(username)}'