import sqlite3
import os.path
from os import remove
import csv
import datetime

# NOTE: uppercase DB denotes database connection object
# whereas lowercase db indicates database cursor object

# modifiable columns
table = ''' CREATE TABLE items(
                barcode     TEXT    NOT NULL,
                room        TEXT    NOT NULL,
                person      TEXT    NOT NULL,
                description TEXT    NOT NULL,
                accounted   INT     NOT NULL,
                datetime    TEXT    NOT NULL,
                roomfound   TEXT    NOT NULL);'''

#region setup
# opens or creates db
def init():
    # if db does not exist...
    if(os.path.isfile('inventory.db') == 0):
        DB = sqlite3.connect('inventory.db')
        DB.execute(table)
    # otherwise, just connect
    else:
        DB = sqlite3.connect('inventory.db')
    DB.commit()
    return DB, DB.cursor()

# queries values for homescreen
# itemTodone, itemTotal, roomTodone, roomTotal
def homeScreen(db):
    progress = []
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
    ##
    return progress


# CLI csv to db
# assumes 4 column csv into db with 0 or '' for rest
def manualIngest(DB, db):
    with open(input("Provide a filename (CSV): "), mode='r') as file:
        inFile = csv.reader(file)
        for lines in inFile:
            print(lines[0])
            db.execute(f"INSERT INTO ITEMS VALUES ('{lines[0]}','{lines[1]}','{lines[2]}','{lines[3]}',0,'','');")
        DB.commit()

# webapp csv upload to db ingest
# returns number of items added
# 'file' is in binary mode, tempFile saves as text
def ingest(file):
    tempFile = open("temp.csv", "w")
    tempFile.write(file.read().decode("utf-8"))
    tempFile.close()
    tempFile = open("temp.csv", "r")
    DB, db = init()
    db.execute("SELECT COUNT(*) FROM items")
    count = -1 * int(db.fetchone()[0]) #fetchone returns a tuple
    inFile = csv.reader(tempFile)
    for lines in inFile:
        try: print(lines[0]) #skips newlines
        except: continue
        db.execute(f"INSERT INTO ITEMS VALUES ('{lines[0]}','{lines[1]}','{lines[2]}','{lines[3]}',0,'','');")
    db.execute("SELECT COUNT(*) FROM items")
    count += int(db.fetchone()[0])
    DB.commit()
    DB.close()
    tempFile.close()
    remove("temp.csv")
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
#endregion

#region roomview
# queries what has and hasn't been found in a certain room
def roomAudit(db, room):
    db.execute(f"SELECT barcode, person, description FROM items WHERE room='{room}' AND accounted=0;")
    todo = db.fetchall()
    db.execute(f"SELECT * FROM items WHERE room='{room}' AND accounted>0")
    todone = db.fetchall()
    todone.append(db.execute(f"SELECT * FROM items WHERE room!='{room}' AND roomfound='{room}'"))
    return todo, todone
#endregion
  
#region reports         
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
    data = db.execute("SELECT barcode, room, accounted, datetime FROM items;")
    rooms = {} # {room: [accounted, total, last_dateTime]}
    roomList = [] # [Room, total, accounted, dateTime]
    for item in data:
        if item[1] not in rooms:
            rooms[item[1]] = [item[2],1,0]
        else:
            rooms[item[1]][0] += item[2]
            rooms[item[1]][1] += 1
            rooms[item[1]][2] = item[3]
    for k, v in rooms.items():
        roomList.append([k, v[1], v[0], v[2]])
    
    return roomList

# finds things in incorrect locationstes 
def wrongSpot(db):
    db.execute("SELECT * FROM items WHERE room!=roomFound AND roomFound!='';")
    return db.fetchall()
#endregion

# main debugging
if __name__ == '__main__':
    DB, db = init()
    file = open("test.csv", 'rb')
    manualIngest(DB, db)
    DB.commit()
    DB.close()