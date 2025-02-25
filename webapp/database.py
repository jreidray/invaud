import sqlite3
from os.path import isfile
from os import remove
from csv import reader as parseCSV
from flask import current_app

# NOTE: uppercase DB denotes database connection object
# whereas lowercase db indicates database cursor object

# columns for SQLite items table
table = ''' CREATE TABLE items(
                barcode     TEXT    NOT NULL,
                room        TEXT    NOT NULL,
                person      TEXT    NOT NULL,
                description TEXT    NOT NULL,
                accounted   INT     NOT NULL,
                datetime    TEXT    NOT NULL,
                roomfound   TEXT    NOT NULL);'''

# open & returns database and cursor object
# creates the database if not found
def init():
    DB = sqlite3.connect(f'{current_app.config["dataDir"]}/inventory.db')
    cursor = DB.cursor()
    cursor.execute("PRAGMA table_info(items);") 
    # checks if table items exists, and creates it if not
    if(cursor.fetchall() == []): cursor.execute(table)
    DB.commit()
    return DB, cursor

# queries values for homescreen
def homeScreen(db):
    progress = [] # [itemTodone, itemTotal, roomTodone, roomTotal]
    db.execute("SELECT COUNT(barcode) FROM items WHERE accounted != 0;")
    progress.append(int(db.fetchone()[0])) # fetch returns a tuple
    db.execute("SELECT COUNT(barcode) FROM items ;")
    progress.append(int(db.fetchone()[0]))
    ## room count
    data = db.execute("SELECT barcode, room, accounted FROM items;")
    complete, total = 0, 0
    rooms = {} # {room: [accounted, total]}
    for item in data:
        if item[1] not in rooms:
            rooms[item[1]] = [item[2],1]
        else:
            rooms[item[1]][0] += item[2]
            rooms[item[1]][1] += 1
    for room in rooms:
        total += 1
        if rooms[room][0] >= rooms[room][1]: complete += 1
    progress.extend([complete,total])
    return progress


# CLI csv to db
# assumes 4 column csv into db with 0 or '' for rest
def manualIngest(DB, db):
    with open(input("Provide a filename (CSV): "), mode='r') as file:
        inFile = parseCSV(file)
        for lines in inFile:
            print(lines[0])
            db.execute(f"INSERT INTO ITEMS VALUES ('{lines[0]}','{lines[1]}','{lines[2]}','{lines[3]}',0,'','');")
        DB.commit()

# webapp csv upload to db ingest
# returns number of items added
# 'file' is in binary mode, tempFile saves as text
def ingest(file):
    tempFile = open(f"{current_app.config['dataDir']}/temp.csv", "w")
    tempFile.write(file.read().decode("utf-8"))
    tempFile.close()
    tempFile = open(f"{current_app.config['dataDir']}/temp.csv", "r")
    DB, db = init()
    db.execute("SELECT COUNT(*) FROM items")
    count = -1 * int(db.fetchone()[0]) #fetchone returns a tuple
    inFile = parseCSV(tempFile)
    for lines in inFile:
        try: print(lines[0]) #skips newlines
        except: continue
        db.execute(f"INSERT INTO ITEMS VALUES ('{lines[0]}','{lines[1]}','{lines[2]}','{lines[3]}',0,'','');")
    db.execute("SELECT COUNT(*) FROM items")
    count += int(db.fetchone()[0])
    DB.commit()
    DB.close()
    tempFile.close()
    remove(f"{current_app.config['dataDir']}/temp.csv")
    return count

# WARNING! This resets all non persistent values
def resetAudit(db):
    print("PRE")
    db.execute("UPDATE items SET accounted=0, datetime='', roomfound='';")
    print("POST")

# WARNING! Removes ALL item entries from database
def resetDB(db):
    print("PRE")
    db.execute("DELETE FROM items;")
    print("POST")

# queries what has and hasn't been found in a certain room
def roomAudit(db, room):
    db.execute(f"SELECT barcode, person, description FROM items WHERE room='{room}' AND accounted=0;")
    todo = db.fetchall()
    db.execute(f"SELECT * FROM items WHERE room='{room}' AND accounted>0")
    todone = db.fetchall()
    todone.append(db.execute(f"SELECT * FROM items WHERE room!='{room}' AND roomfound='{room}'"))
    return todo, todone
  
# finds items that have not been found yet (accounted == 0)
def notFound(db):
    db.execute("SELECT barcode, room, person, description FROM items WHERE accounted=0;")
    return db.fetchall()

# finds items that have been found more than once (accounted > 1)
def overFound(db):
    db.execute("SELECT barcode, accounted, room, roomfound, datetime FROM items WHERE accounted>1;")
    return db.fetchall()

# finds rooms that haven't been fully scanned
def underRoom(db):
    data = db.execute("SELECT barcode, room, accounted, datetime FROM items;")
    rooms = {} # {room: [accounted, total, last_dateTime]}
    roomList = [] # [Room, total, accounted, dateTime]
    for item in data:
        if item[1] not in rooms:
            rooms[item[1]] = [item[2],1,'']
        else:
            rooms[item[1]][0] += item[2]
            rooms[item[1]][1] += 1
            rooms[item[1]][2] = item[3]
    for k, v in rooms.items():
        if v[0] != v[1]:
            roomList.append([k, v[1], v[0], v[2]])
    
    return roomList

# finds things in incorrect locations 
def wrongSpot(db):
    db.execute("SELECT * FROM items WHERE room!=roomFound AND roomFound!='';")
    return db.fetchall()
