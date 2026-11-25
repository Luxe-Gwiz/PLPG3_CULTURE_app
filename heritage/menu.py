from .roles import CREATE, DELETE, READ, ROLES, UPDATE
from .services import EVENTS, TRADITIONS
from .validators import clean_date, clean_record_id, clean_text

DIVIDER = "-" * 70
MENU_LINES = [
    "  1. Add a cultural tradition",
    "  2. Record a cultural event",
    "  3. View saved records",
    "  4. Search records",
    "  5. Update a record",
    "  6. Delete a record",
    "  0. Exit",
]
PERMISSION_WORDS = {CREATE: "add", UPDATE: "update", DELETE: "delete"}
TRADITION_LABELS = [("Community", "community"), ("Description", "description"), ("Recorded by", "created_by")]
EVENT_LABELS = [("Date", "event_date"), ("Location", "location"), ("Recorded by", "created_by")]


def check(field, raw, service=None, record_id=None):
    if field == "Event date":
        return clean_date(raw)
    if field == "Record ID":
        return clean_record_id(raw)
    if field == "Description":
        return service.check_description_available(raw, record_id)
    return clean_text(raw, field)


def ask(prompt, field, current=None, service=None, record_id=None):
    while True:
        if current is None:
            raw = input(prompt)
        else:
            raw = input(f"{prompt} [{current}]: ")
            if not raw.strip():
                return current
        try:
            return check(field, raw, service, record_id)
        except ValueError as exc:
            print(f"  ! {exc} Please try again.")


def choose_role():
    print("\nWelcome to the Community Culture & Heritage Manager.")
    print("Select your role:")
    for i in range(len(ROLES)):
        print(f"  {i + 1}. {ROLES[i]}")
    while True:
        choice = input("Enter role number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(ROLES):
            return ROLES[int(choice) - 1]
        print("  ! Invalid choice. Enter a number from the list.")


def pick_table(verb):
    print(f"\nWhich type of record do you want to {verb}?")
    print("  1. Cultural tradition")
    print("  2. Cultural event")
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            return TRADITIONS
        if choice == "2":
            return EVENTS
        print("  ! Please enter 1 or 2. Please try again.")


def print_records(rows, noun, title, labels):
    if not rows:
        print(f"  (no {noun}s found)")
    for row in rows:
        print(DIVIDER)
        print(f"  [{noun.capitalize()} #{row['id']}] {row[title]}")
        for label, key in labels:
            print(f"     {label:<11} : {row[key]}")


class HeritageCLI:
    def __init__(self, service):
        self.service = service

    def run(self):
        while True:
            print()
            print("==================== Community Culture & Heritage ====================")
            print(f"  Logged in as: {self.service.role}")
            for line in MENU_LINES:
                print(line)
            print("======================================================================")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("\nThank you for preserving our culture. Goodbye!")
                return
            if choice not in ["1", "2", "3", "4", "5", "6"]:
                print("  ! Invalid choice. Please select an option from the menu.")
                continue
            try:
                self.run_option(choice)
            except ValueError as exc:
                print(f"  ! {exc}")

    def run_option(self, choice):
        if choice == "1":
            self.add_tradition()
        elif choice == "2":
            self.record_event()
        elif choice == "3":
            self.view_records()
        elif choice == "4":
            self.search_records()
        elif choice == "5":
            self.update_record()
        else:
            self.delete_record()

    def need(self, permission):
        if not self.service.can(permission):
            raise ValueError(f"Your role cannot {PERMISSION_WORDS[permission]} records.")

    def add_tradition(self):
        self.need(CREATE)
        print("\n--- Add a cultural tradition ---")
        name = ask("Tradition name: ", "Tradition name")
        community = ask("Community: ", "Community")
        description = ask("Description: ", "Description", service=self.service)
        new_id = self.service.add_tradition(name, community, description)
        print(f"  Saved! Tradition #{new_id} '{name}' has been recorded.")

    def record_event(self):
        self.need(CREATE)
        print("\n--- Record a cultural event ---")
        event_name = ask("Event name: ", "Event name")
        event_date = ask("Event date (YYYY-MM-DD): ", "Event date")
        location = ask("Location: ", "Location")
        new_id = self.service.add_event(event_name, event_date, location)
        print(f"  Saved! Event #{new_id} '{event_name}' has been recorded.")

    def view_records(self):
        print("\n--- Saved traditions ---")
        print_records(self.service.list_records(TRADITIONS), "tradition", "name", TRADITION_LABELS)
        print("\n--- Saved events ---")
        print_records(self.service.list_records(EVENTS), "event", "event_name", EVENT_LABELS)

    def search_records(self):
        keyword = ask("Search keyword: ", "Keyword")
        print(f"\n--- Traditions matching '{keyword}' ---")
        print_records(self.service.list_records(TRADITIONS, keyword), "tradition", "name", TRADITION_LABELS)
        print(f"\n--- Events matching '{keyword}' ---")
        print_records(self.service.list_records(EVENTS, keyword), "event", "event_name", EVENT_LABELS)

    def update_record(self):
        self.need(UPDATE)
        table = pick_table("update")
        record_id = ask("Record ID to update: ", "Record ID")
        record = self.service.get_record(table, record_id)
        print(DIVIDER)
        print("Press Enter to keep the current value shown in brackets.")
        if table == TRADITIONS:
            name = ask("Tradition name", "Tradition name", record["name"])
            community = ask("Community", "Community", record["community"])
            description = ask("Description", "Description", record["description"], self.service, record_id)
            self.service.update_tradition(record_id, name, community, description)
        else:
            event_name = ask("Event name", "Event name", record["event_name"])
            event_date = ask("Event date", "Event date", record["event_date"])
            location = ask("Location", "Location", record["location"])
            self.service.update_event(record_id, event_name, event_date, location)
        print(f"  Record #{record_id} has been updated.")

    def delete_record(self):
        self.need(DELETE)
        table = pick_table("delete")
        record_id = ask("Record ID to delete: ", "Record ID")
        record = self.service.get_record(table, record_id)
        if table == TRADITIONS:
            label = record["name"]
        else:
            label = record["event_name"]
        confirm = input(f"  Type 'yes' to permanently delete '{label}': ").strip().lower()
        if confirm != "yes":
            print("  Deletion cancelled.")
            return
        self.service.delete_record(table, record_id)
        print(f"  Record #{record_id} has been deleted.")
