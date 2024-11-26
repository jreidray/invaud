from flask import Blueprint, redirect, render_template, url_for
from . import database
from .auth import authorized

reports = Blueprint('reports', __name__)

# shows list of availible reports
@reports.route("/")
def reportsView():
    return render_template('reports.html') if authorized() else redirect(url_for('auth.login'))

# shows items found multiple times
@reports.route("/extras/")
def extrasView():
    DB, db = database.init()
    items = database.overFound(db)
    DB.close()
    return render_template('extra.html', items=items) if authorized() else redirect(url_for('auth.login'))

# shows rooms where not everything has been found
@reports.route("/incomplete/")
def incompleteView():
    DB, db = database.init()
    items = database.underRoom(db)
    DB.close()
    return render_template('incomplete.html', items=items) if authorized() else redirect(url_for('auth.login'))

# shows items found in the wrong place
@reports.route("/misplaced/")
def misplacedView():
    DB, db = database.init()
    items = database.wrongSpot(db)
    DB.close()
    return render_template('misplaced.html', items=items) if authorized() else redirect(url_for('auth.login'))

# shows items that have not been found
@reports.route("/missing/")
def missingView():
    DB, db = database.init()
    items = database.notFound(db)
    DB.close()
    return render_template('missing.html', items=items) if authorized() else redirect(url_for('auth.login'))
