# Community Culture & Heritage Manager

A menu-driven Python command-line program that records cultural traditions and events in a SQLite database. Users can add, view, search, update, and delete records, depending on their role.


## 1. Why this app exists

Traditions, songs, and dances disappear when nobody writes them down. Many communities keep their history only on paper or in memory, which makes it hard to find and manage. This app keeps those records in one place.

It connects to two GCGOs:

- **Governance:** helps community members organize activities and keep accurate records.
- **Arts, Design and Culture:** preserves traditions, festivals, music, and dance.

## 2. What the app does

| Option | Action | What it does |
|---|---|---|
| 1 | Add | Records a tradition: name, community, and a unique description |
| 2 | Add | Records an event: name, date, and location |
| 3 | View | Shows every saved tradition and event |
| 4 | Search | Finds records by a word in the name, community, or location |
| 5 | Update | Changes a record. Press Enter to keep a value |
| 6 | Delete | Removes a record after you type `yes` |
| 0 | Exit | Closes the program |

## 3. Roles

The role is chosen once, when the program starts. It cannot be changed during a session. Each saved record shows the role that created it.

| Role | Add | View and search | Update | Delete |
|---|:---:|:---:|:---:|:---:|
| Head of Culture | Yes | Yes | Yes | Yes |
| Culture Chief | Yes | Yes | Yes | No |
| Local Member | Yes | Yes | No | No |

The prototype has no passwords, so roles guide how the app is used. They don't prove who the user is.

## 4. How the system is built

The code is split into layers, and each layer does one job:

1. **User interface** (`heritage/menu.py`, `heritage/roles.py`): shows the menu, asks questions, and prints results. It never writes SQL.
2. **Database** (`heritage/services.py`, `heritage/validators.py`, `heritage/database.py`): checks the role and the values, applies the rules, and reads and writes the SQLite file.
3. **Error handling**: every problem is raised as a `ValueError` with a short message. The menu catches it, prints the message, and shows the menu again.
4. **Main program** (`main.py`): opens the database, asks for a role, runs the menu, and closes the database.

Each layer only calls the layer below it: `main.py` → `menu.py` → `services.py` → `validators.py` and `database.py`.

## 5. Adding a tradition or an event

- **Tradition:** enter a name, a community, and a description. The description must be unique, ignoring capital letters. Names and communities may repeat.
- **Event:** enter a name, a date, and a location. The date must be a real day in `YYYY-MM-DD` form.

The flow is: choose `1` or `2`, type each detail, the program checks it, the record is saved with a number, and the menu returns.

## 6. Database and SQLite

All records are stored in one file, `heritage.db`, which is created automatically the first time the app runs.

The file holds two tables:

- `traditions`: `id`, `name`, `community`, `description`, `created_by`
- `events`: `id`, `event_name`, `event_date`, `location`, `created_by`

On each start, the program creates the tables only if they don't exist, so saved data is kept. Every add, update, and delete is written and confirmed. Searches and lists read the matching rows.

To use a different file, set the `HERITAGE_DB` environment variable before you run the program.

## 7. How main starts the system

1. Opens the database. If it cannot open, a message is shown and the program stops.
2. Asks the user to choose a role.
3. Connects the role and the database through the service layer.
4. Starts the menu, which keeps running until the user chooses 0.
5. Closes the database, even if an error or Ctrl+C happens.

## 8. Files

```
PLPG3_CULTURE_app/
├── main.py                 Starts the program and closes it
├── README.md               This guide
├── .gitignore              Files Git should ignore (for example *.db)
└── heritage/
    ├── menu.py             User interface: menu, questions, results
    ├── roles.py            Roles and what each role may do
    ├── services.py         Features: add, view, search, update, delete
    ├── validators.py       Checks each value
    └── database.py         Opens SQLite, creates tables, runs queries
```

## 9. Running the program

From the project folder:

```bash
python main.py
```

To keep the database somewhere else:

```bash
HERITAGE_DB=/full/path/to/heritage.db python main.py
```

Requirements: Python 3. No extra packages are needed, since `sqlite3` comes with Python.

## 10. Team and assignments

| Project area | File | Member |
|---|---|---|
| User interface | menu.py | Davina |
| User interface | roles.py | Calvin |
| Database | database.py | Luxe |
| Database | services.py | Adriel |
| Database | validators.py | Calvin |
| Error handling | (built into each file as ValueError) | Luxe |
| General program | main.py | Deng |

## 11. Course topics used

- **Data structures:** lists and dictionaries (the roles, the permissions, the menu lines, and the column names).
- **Conditionals:** `if`, `elif`, and `else` for menu choices and checks.
- **Loops:** `while` loops that keep asking until input is valid, and `for` loops that print records.
- **Functions:** each task is a small function.
- **Classes:** `Database`, `HeritageService`, and `HeritageCLI`.
- **SQL:** `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, and `LIKE`, with `?` placeholders.
- **Exceptions:** `try` and `except` to catch bad input and database problems.
