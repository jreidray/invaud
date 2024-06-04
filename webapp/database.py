import sqlite3
import os.path
import csv
import datetime

# NOTE: uppercase DB denotes database connection object
# whereas lowercase db indicates database cursor object

# modifiable columns
table = ''' CREATE TABLE items(
                barcode     INT     NOT NULL,
                room        TEXT    NOT NULL,
                person      TEXT    NOT NULL,
                description TEXT    NOT NULL,
                accounted   INT     NOT NULL,
                datetime    TEXT    NOT NULL,
                roomfound   TEXT    NOT NULL);'''

# opens or creates db
def init():
    # if db does not exist...
    if(os.path.isfile('inventory.db') == 0):
        DB = sqlite3.connect('inventory.db')
        DB.execute(table)
    # otherwise, just connect
    else:
        DB = sqlite3.connect('inventory.db')
    return DB, DB.cursor()

# takes csv input into db
# assumes 4 column csv into db with 0 or '' for rest
def ingest(DB, db):
    with open(input("Provide a filename (CSV): "), mode='r') as file:
        inFile = csv.reader(file)
        for lines in inFile:
            db.execute(f"INSERT INTO ITEMS VALUES ({lines[0]},{lines[1]},{lines[2]},{lines[3]},0,'','');")
        DB.commit()
            
# finds items that have not been found yet (accounted == 0)
def notFound(db):
    db.execute("SELECT barcode, room, person, description FROM items WHERE accounted=0;")
    return db.fetchall()

# finds items that have been found more than once (accounted > 1)
def overFound(db):
    db.execute("SELECT barcode, room, roomfound, datetime FROM items WHERE accounted>1;")
    return db.fetchall()

# finds rooms that haven't been fully scanned
def underRoom(db):
    db.execute("SELECT room, accounted, datetime, FROM items;")
    items = db.fetchall()
    rooms = {}
    roomList = []

    # creates a dictionary with each room's stats    
    # {"ROOM": [Count, Found, Date]}
    for item in items:
        # if room hasn't been seen yet, set it up
        if item[0] not in rooms:
            rooms[item[0]] = [1, item[1], item[2]]
        # if room has been seen yet, increment
        else:
            # take the newest datetime
            if rooms[item[0]] > item[2]: dt = rooms[item[0]]
            else: dt = item[2]
            rooms[item[0]] = [rooms[item[0]]+1, rooms[item[1]]+item[1], dt]

    # makes a list instead of a dict
    # [Room, Count, Found, Date]
    for k, v in rooms.items():
        roomList.append([k, v[0], v[1], v[2]])

    return roomList

# finds things in incorrect locations 
def wrongSpot(db):
    db.execute("SELECT * FROM items WHERE room!=roomFound AND roomFound!='';")
    return db.fetchall()

# WARNING! This resets all non persistent values
def resetAudit(db):
    db.execute("UPDATE items SET accounted=0, datetime='', roomfound='';")

# main debugging
if __name__ == '__main__':
    DB, db = init()
    #ingest(db)
    DB.commit()
    DB.close()