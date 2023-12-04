-- Enable logging for all SQL statements
PRAGMA journal_mode = WAL;
PRAGMA wal_autocheckpoint = 1;
PRAGMA wal_checkpoint(FULL);

-- Enable query execution logging
PRAGMA temp_store = 2;
PRAGMA cache_size = -8000;
PRAGMA fullfsync = 1;


CREATE TABLE IF NOT EXISTS Item (
    ItemId INTEGER PRIMARY KEY,
    ItemName TEXT,
    ChecklistId INT
);

CREATE TABLE IF NOT EXISTS Checklist (
    ChecklistId INTEGER PRIMARY KEY,
    ChecklistName TEXT UNIQUE
);
