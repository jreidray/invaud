import flask
from . import database

views = flask.Blueprint('views', __name__)

#region /
@views.route("/")
def homeView():
    return "<h1>Homepage</h1>"

@views.route("/ingest/")
def ingestView():
    return flask.render_template("ingest.html")

@views.route("/ingestSuccess/", methods=["POST"])
def ingestSuccess():
    if flask.request.method == "POST":
        file = flask.request.files['file']
        count = database.ingest(file)
        return flask.render_template("ingestSuccess", count=count)
#endregion

#region /room/
@views.route('/room/<room>/', methods=["GET", "POST"])
def roomView(room):
    if flask.request.method == "POST":
        text = flask.request.form.get("textInput")
    else:
        DB, db = database.init()
        todo, todone = database.roomAudit(db, room)
        return flask.render_template("room.html", room=room, todo=todo, todone=todone)

#endregion

#region /item/

#endregion

#region /reports/
@views.route("/reports/extras/")
def extrasView():
    DB, db = database.init()
    items = database.overFound(db)
    DB.close()
    return flask.render_template('extra.html', items=items)

@views.route("/reports/incomplete/")
def incompleteView():
    DB, db = database.init()
    items = database.underRoom(db)
    DB.close()
    return flask.render_template('incomplete.html', items=items)

@views.route("/reports/misplaced/")
def misplacedView():
    DB, db = database.init()
    items = database.wrongSpot(db)
    DB.close()
    return flask.render_template('misplaced.html', items=items)

@views.route("/reports/missing/")
def missingView():
    DB, db = database.init()
    items = database.notFound(db)
    DB.close()
    return flask.render_template('missing.html', items=items)
#endregion

