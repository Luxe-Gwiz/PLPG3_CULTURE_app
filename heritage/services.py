import sqlite3

from .roles import CREATE, DELETE, READ, UPDATE, has_permission
from .validators import MAX_LONG_TEXT, clean_date, clean_record_id, clean_text

TRADITIONS = "traditions"
EVENTS = "events"
COLUMNS = {
    TRADITIONS: ["id", "name", "community", "description", "created_by"],
    EVENTS: ["id", "event_name", "event_date", "location", "created_by"],
}
LIST_ALL = {
    TRADITIONS: "SELECT id, name, community, description, created_by FROM traditions ORDER BY id",
    EVENTS: "SELECT id, event_name, event_date, location, created_by FROM events ORDER BY event_date, id",
}
LIST_MATCH = {
    TRADITIONS: "SELECT id, name, community, description, created_by FROM traditions "
                "WHERE name LIKE ? OR community LIKE ? ORDER BY id",
    EVENTS: "SELECT id, event_name, event_date, location, created_by FROM events "
            "WHERE event_name LIKE ? OR location LIKE ? ORDER BY event_date, id",
}


def to_dicts(columns, rows):
    records = []
    for row in rows:
        record = {}
        for i in range(len(columns)):
            record[columns[i]] = row[i]
        records.append(record)
    return records


class HeritageService:
    def __init__(self, db, role):
        self.db = db
        self.role = role

    def can(self, permission):
        return has_permission(self.role, permission)

    def _require(self, permission):
        if not self.can(permission):
            raise ValueError(f"The role '{self.role}' is not allowed to {permission} records.")

    def _check_table(self, table):
        if table not in COLUMNS:
            raise ValueError(f"Unknown table: {table}")

    def _write(self, sql, params=()):
        try:
            self.db.execute(sql, params)
        except sqlite3.Error as exc:
            raise ValueError(f"Could not save changes: {exc}")

    def _read(self, sql, params=()):
        try:
            return self.db.fetch_all(sql, params)
        except sqlite3.Error as exc:
            raise ValueError(f"Could not read records: {exc}")

    def _last_id(self, table):
        return self._read(f"SELECT MAX(id) FROM {table}")[0][0]

    def check_description_available(self, description, exclude_id=None):
        description = clean_text(description, "Description", MAX_LONG_TEXT)
        for row in self._read("SELECT id, description FROM traditions"):
            if row[1].lower() == description.lower() and row[0] != exclude_id:
                raise ValueError("This description is already used by another tradition.")
        return description

    def add_tradition(self, name, community, description):
        self._require(CREATE)
        name = clean_text(name, "Tradition name")
        community = clean_text(community, "Community")
        description = self.check_description_available(description)
        self._write(
            "INSERT INTO traditions (name, community, description, created_by) VALUES (?, ?, ?, ?)",
            (name, community, description, self.role),
        )
        return self._last_id(TRADITIONS)

    def add_event(self, event_name, event_date, location):
        self._require(CREATE)
        event_name = clean_text(event_name, "Event name")
        event_date = clean_date(event_date)
        location = clean_text(location, "Location")
        self._write(
            "INSERT INTO events (event_name, event_date, location, created_by) VALUES (?, ?, ?, ?)",
            (event_name, event_date, location, self.role),
        )
        return self._last_id(EVENTS)

    def list_records(self, table, keyword=None):
        self._require(READ)
        self._check_table(table)
        if keyword:
            pattern = f"%{keyword.strip()}%"
            rows = self._read(LIST_MATCH[table], (pattern, pattern))
        else:
            rows = self._read(LIST_ALL[table])
        return to_dicts(COLUMNS[table], rows)

    def get_record(self, table, record_id):
        self._require(READ)
        self._check_table(table)
        record_id = clean_record_id(record_id)
        rows = self._read(f"SELECT * FROM {table} WHERE id = ?", (record_id,))
        if not rows:
            raise ValueError(f"No record with ID {record_id} was found.")
        return to_dicts(COLUMNS[table], rows)[0]

    def update_tradition(self, record_id, name, community, description):
        self._require(UPDATE)
        record_id = self.get_record(TRADITIONS, record_id)["id"]
        name = clean_text(name, "Tradition name")
        community = clean_text(community, "Community")
        description = self.check_description_available(description, record_id)
        self._write(
            "UPDATE traditions SET name = ?, community = ?, description = ? WHERE id = ?",
            (name, community, description, record_id),
        )

    def update_event(self, record_id, event_name, event_date, location):
        self._require(UPDATE)
        record_id = self.get_record(EVENTS, record_id)["id"]
        event_name = clean_text(event_name, "Event name")
        event_date = clean_date(event_date)
        location = clean_text(location, "Location")
        self._write(
            "UPDATE events SET event_name = ?, event_date = ?, location = ? WHERE id = ?",
            (event_name, event_date, location, record_id),
        )

    def delete_record(self, table, record_id):
        self._require(DELETE)
        record_id = self.get_record(table, record_id)["id"]
        self._write(f"DELETE FROM {table} WHERE id = ?", (record_id,))
