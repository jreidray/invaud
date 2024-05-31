# invaud

Inventory Auditing app by Jeremy Ray

## Web app

TBD

## Database

Running SQLite via Python, holds the inventoried items and their attributes. Queries can reveal issues and anomalies (items not found or found too many times, rooms missing things or with extra things, etc).

### 'Items' table

Barcode - Integer - Persistent - The assigned barcode number.
Room - Text - Persistent - The assigned room (should match a Room object).
Person - Text - Persistent - The person which the item is assigned to (should match a Person object).
Description - Text - Persistent - Description of the object pulled from inventory database.
Notes - Text - Semipersistent - Just general notes you can add at will, or chose to be cleared. Think of *where* in the room something is, or location of it's barcode.
Accounted - Integer - Nonpersistent - How *many* of the items have been found. Resets to zero for a new audit; should be 1 when found; will be an error when more than 1 has been found.
Datetime - Text - Nonpersistent - The date and time(s) which the item was found. Appends to value (multiple finds = multiple dates) and is reset during a new audit.
RoomFound - Text - Nonpersistent - The last room(s) scanned before the item was found. Appends and is reset for new audit.
