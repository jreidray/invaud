# invaud

Inventory Auditing app by Jeremy Ray

## Webapp

The webserver can either be run in Flask's development server with the start.py script, or HTTPS encrypted with Apache via the invaud.conf site pointing to the invaud.wsgi interface. Both interface with the /webapp/ module that initializes the Flask app, the SQLite3 database, and the Jinja blueprints. Jinja, built into Flask, renders the HTML in /templates which contain Python code themselves.

## Database

Running SQLite via Python, holds the inventoried items and their attributes. Queries can reveal issues and anomalies (items not found or found too many times, rooms missing things or with extra things, etc). Other more complex data is extrapolated in Python for when queries would not suffice.

### 'Items' table

Barcode - Integer - Persistent - The assigned barcode number.

Room - Text - Persistent - The assigned room (should match a Room object).

Person - Text - Persistent - The person which the item is assigned to (should match a Person object).

Description - Text - Persistent - Description of the object pulled from inventory database. User added notes will be prepended.

Accounted - Integer - Nonpersistent - How *many* of the items have been found. Resets to zero for a new audit; should be 1 when found; will be an error when more than 1 has been found.

Datetime - Text - Nonpersistent - The date and time(s) which the item was found. Appends to value (multiple finds = multiple dates) and is reset during a new audit.

RoomFound - Text - Nonpersistent - The last room(s) scanned before the item was found. Appends and is reset for new audit.
