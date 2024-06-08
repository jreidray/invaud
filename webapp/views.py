import flask
import datetime
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
        return flask.render_template("ingestSuccess.html", count=count)
#endregion

#region /room/
@views.route('/room/', methods=["GET", "POST"])
def roomView():
    if flask.request.method == "POST":
        return flask.redirect(flask.url_for('views.roomAudit', room = flask.request.form.get("textInput")))
    else:
        return flask.render_template("room.html")

@views.route('/room/<room>/', methods=["GET", "POST"])
def roomAudit(room):
    DB, db = database.init()
    if flask.request.method == "POST":
        item = flask.request.form.get("textInput")
        date = datetime.datetime.now().strftime("%c")
        db.execute(f"UPDATE items SET accounted=accounted+1, datetime='{date}', roomFound='{room}' WHERE barcode='{item}';")
    todo, todone = database.roomAudit(db, room)
    DB.commit()
    DB.close()
    return flask.render_template("roomAudit.html", room=room, todo=todo, todone=todone)

#endregion

#region /item/
@views.route('/item/', methods=["GET", "POST"])
def itemView():
    if flask.request.method == "POST":
        return flask.redirect(flask.url_for('views.itemAudit', item = flask.request.form.get("textInput")))
    else:
        return flask.render_template("item.html")

@views.route('/item/<item>/', methods=["GET", "POST"])
def itemAudit(item):
    DB, db = database.init()
    db.execute(f"SELECT * FROM items WHERE barcode='{item}';")
    items = db.fetchone()
    if flask.request.method == "POST":
        room = flask.request.form.get("textInput")
        date = datetime.datetime.now().strftime("%c")
        db.execute(f"UPDATE items SET accounted=accounted+1, roomfound='{room}', datetime='{date}' WHERE barcode='{item}';")
        DB.commit()
        DB.close()
        return flask.redirect(flask.url_for('views.itemAudit', item=item))
    DB.close()
    return flask.render_template("itemAudit.html", item=item, items=items)


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

