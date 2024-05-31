import sqlite3
import os.path
import csv

# NOTE: uppercase DB denotes database connection object
# whereas lowercase db indicates database cursor object

# modifiable columns
table = ''' CREATE TABLE items(
                barcode     INT     NOT NULL,
                room        TEXT    NOT NULL,
                person      TEXT    NOT NULL,
                description TEXT    NOT NULL,
                notes       TEXT    NOT NULL,
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
def ingest(db):
    with open(input("Provide a filename (CSV): "), mode='r') as file:
        inFile = csv.reader(file)
        for lines in inFile:
            db.execute(f"INSERT INTO ITEMS VALUES ({lines[0]},{lines[1]},{lines[2]},{lines[3]},'',0,'','');")
            
# finds items that have not been found yet (accounted == 0)
def notFound(db):
    db.execute("SELECT * FROM items WHERE accounted=0;")
    return db.fetchall()

# finds items that have been found more than once (accounted > 1)
def overFound(db):
    db.execute("SELECT * FROM items WHERE accounted>1;")
    return db.fetchall()

# finds rooms that haven't been fully scanned
def underRoom(db):
    db.execute("SELECT * FROM items;")
    all = db.fetchall()
    rooms = {}
    # checks each item in table, if not accounted for, then increments the room's value in rooms dictionary
    for item in all:
        if item[5]==0 or item[5]=='None':
            try:
                rooms[item[1]] += 1
            except:
                rooms[item[1]] = 1
    return rooms

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