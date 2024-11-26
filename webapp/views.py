from flask import Blueprint, redirect, render_template, request, url_for
from datetime import datetime
from . import database
from .auth import authorized

views = Blueprint('views', __name__)

# shows homescreen with progress & reports
@views.route("/")
def homeView():
    DB, db = database.init()
    [itemTodone, itemTotal, roomTodone, roomTotal] = database.homeScreen(db)
    DB.close()
    return render_template('home.html', itemProgress=divByZero(itemTodone,itemTotal), roomProgress=divByZero(roomTodone,roomTotal), itemTodone=itemTodone, itemTotal=itemTotal, roomTodone=roomTodone, roomTotal=roomTotal) if authorized() else redirect(url_for('auth.login'))

# ingests data in CSV format
@views.route("/ingest/")
def ingestView():
    return render_template("ingest.html") if authorized() else redirect(url_for('auth.login'))

# confirms successful data ingest
@views.route("/ingestSuccess/", methods=["POST"])
def ingestSuccess():
    if request.method == "POST" and authorized():
        file = request.files['file']
        count = database.ingest(file)
        return render_template("ingestSuccess.html", count=count) if authorized() else redirect(url_for('auth.login'))

# shows option to reset data
@views.route("/reset/")
def resetConfirmation():
    return render_template("reset.html") if authorized() else redirect(url_for('auth.login'))

# resets audit data (last 3 columns)
@views.route("/auditReset/")
def auditReset():
    # auth before reset
    if authorized():
        DB, db = database.init()
        database.resetAudit(db)
        DB.commit()
        DB.close()
        return render_template("resetSuccess.html", reset="All audit entries")
    return redirect(url_for('auth.login'))

# resets entire SQL table
@views.route("/dbReset/")
def dbReset():
    # auth before reset
    if authorized():
        DB, db = database.init()
        database.resetDB(db)
        DB.commit()
        DB.close()
        return render_template("resetSuccess.html", reset="All data entries") 
    return redirect(url_for('auth.login'))

# gets input to audit a room
@views.route('/room/', methods=["GET", "POST"])
def roomView():
    if request.method == "POST" and authorized():
        text = request.form.get("textInput")
        return redirect(url_for('views.roomAudit', room = text))
    else:
        return render_template("room.html") if authorized() else redirect(url_for('auth.login'))

# shows info on specified room
@views.route('/room/<room>/', methods=["GET", "POST"])
def roomAudit(room):
    DB, db = database.init()
    if request.method == "POST" and authorized():
        item = request.form.get("textInput")
        date = datetime.now().strftime("%c")
        db.execute(f"UPDATE items SET accounted=accounted+1, datetime='{date}', roomFound='{room}' WHERE barcode='{item}';")
    todo, todone = database.roomAudit(db, room)
    DB.commit()
    DB.close()
    return render_template("roomAudit.html", room=room, todo=todo, todone=todone) if authorized() else redirect(url_for('auth.login'))
   
# gets input to audit an item
@views.route('/item/', methods=["GET", "POST"])
def itemView():
    if request.method == "POST" and authorized():
        text = request.form.get("textInput")
        return redirect(url_for('views.itemAudit', item = text))
    else:
        return render_template("item.html") if authorized() else redirect(url_for('auth.login'))

# shows info on specified item
@views.route('/item/<item>/', methods=["GET", "POST"])
def itemAudit(item):
    DB, db = database.init()
    db.execute(f"SELECT * FROM items WHERE barcode='{item}';")
    items = db.fetchone()
    if request.method == "POST" and authorized():
        room = request.form.get("textInput")
        date = datetime.now().strftime("%c")
        db.execute(f"UPDATE items SET accounted=accounted+1, roomfound='{room}', datetime='{date}' WHERE barcode='{item}';")
        DB.commit()
        DB.close()
        return redirect(url_for('views.itemAudit', item=item))
    DB.close()
    return render_template("itemAudit.html", item=item, items=items) if authorized() else redirect(url_for('auth.login'))

# prevents errors on homescreen when no inventory data is present
def divByZero(numer,denom):
    try: return int(numer/denom*100)
    except: return 0
