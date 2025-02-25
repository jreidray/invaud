# invaud

Inventory Auditing app by Jeremy Ray for Mississippi State University's Social Science Research Center

This app is built in Flask, a Python web development framework which uses the Jinja HTML template rendering system. Python SQLite3 is used as the database, where the inventory records are stored locally. Password authentication is required to enter the site' from there, you can upload a .csv of your inventory with the given columns. The homepage shows the status of your 'audit', where you visit each room of your department and scan every piece of inventoried equipment. There are also several report views, including items found too many or too few times, and rooms with incomplete audits or extraneous items. After your audit, the counts can be reset without deleting inventory entries. 

## Deployment Options

Be sure to edit the enviornment variables before building and deploying to set your password. SSL encryption is prefered; cert-bot or Nginx Proxy Manager (NPM) can handle your certificates and renewal.

- Docker. `docker build -t invaud:latest .` from the root directory. Serve behind a reverse proxy like NPM. Mount the `/data` volume to access the inventory.db backup.
- Apache. Move and enable `invaud.conf` into `/etc/apache2/sites-enabled/` and change the directory to match the `invaud.wsgi` location.
- Flask. The Flask development server is only meant as means to locally test apps; not recommended. Run `start.py`.

### 'Items' table

Barcode - Integer - Persistent - The assigned barcode number.

Room - Text - Persistent - The assigned room (should match a Room object).

Person - Text - Persistent - The person which the item is assigned to (should match a Person object).

Description - Text - Persistent - Description of the object pulled from inventory database. User added notes will be prepended.

Accounted - Integer - Nonpersistent - How *many* of the items have been found. Resets to zero for a new audit; should be 1 when found; will be an error when more than 1 has been found.

Datetime - Text - Nonpersistent - The date and time(s) which the item was found. Appends to value (multiple finds = multiple dates) and is reset during a new audit.

RoomFound - Text - Nonpersistent - The last room(s) scanned before the item was found. Appends and is reset for new audit.
