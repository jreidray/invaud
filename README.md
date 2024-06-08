# invaud

Inventory Auditing app by Jeremy Ray

## Webapp

The webserver is setup with Flask on Python. The start.py file is the script that starts the server from the custom module /webapp/. In the webapp module, there is the \_\_init\_\_.py (registers config data), database.py (detailed below), views.py (URL Blueprints), and the /templates/ folder. Templates are HTML files written with Jinja that is rendered by Flask and served to the user. These templates can run Python code inside (IE for loop to generate rows of a table). 

## Database

Running SQLite via Python, holds the inventoried items and their attributes. Queries can reveal issues and anomalies (items not found or found too many times, rooms missing things or with extra things, etc).

### 'Items' table

Barcode - Integer - Persistent - The assigned barcode number.

Room - Text - Persistent - The assigned room (should match a Room object).

Person - Text - Persistent - The person which the item is assigned to (should match a Person object).

Description - Text - Persistent - Description of the object pulled from inventory database. User added notes will be prepended.

Accounted - Integer - Nonpersistent - How *many* of the items have been found. Resets to zero for a new audit; should be 1 when found; will be an error when more than 1 has been found.

Datetime - Text - Nonpersistent - The date and time(s) which the item was found. Appends to value (multiple finds = multiple dates) and is reset during a new audit.

RoomFound - Text - Nonpersistent - The last room(s) scanned before the item was found. Appends and is reset for new audit.
