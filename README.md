# iasm_system
Inventory and Sales Management System

## Midterm Project (SQLite + Tkinter)

This project implements the required Inventory and Sales Management System for CPRO 2201.

### Tech Stack
- Python 3.13
- SQLite (`sqlite3` from Python standard library)
- Tkinter GUI

### Project Structure
- `app.py` - Tkinter user interface (no SQL inside)
- `models.py` - `Product`, specialized product classes, and `Sale`
- `inventory.py` - `Inventory` dictionary management + service layer
- `db.py` - all database initialization and CRUD/query logic
- `schema.sql` - database schema script
- `inventory.db` - SQLite file (auto-created at first run)

### How to Run
1. Open a terminal in the project folder.
2. Run:

```bash
python app.py
```

The database is created automatically using `schema.sql` on first launch.
