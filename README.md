# Coding Session Tracker

Coding Session Tracker is a local Python application for recording short coding-session notes, each automatically numbered and dated. It provides a PySide6 desktop widget and a terminal interface.

I built it as a one-month learning project focused on OOP, JSON persistence, agentic coding, and desktop development with PySide6.

## Features

- Add automatically numbered and dated session notes.
- Search active sessions by number, note keyword, or date.
- Combine search values in the desktop interface.
- Update notes or archive sessions without reusing their numbers.
- Use the desktop interface in floating, windowed, or hidden mode.
- Adjust its position, opacity, theme, always-on-top behavior, and compact layout.
- Perform one operation per launch through the terminal interface.

## Quick Start

### Requirements

- Python 3.10–3.14
- A graphical desktop and system tray for the desktop interface

### Installation

```bash
git clone https://github.com/FelixZimmermannDev/session-notes.git
cd session-notes
python -m venv .venv
```

Activate the virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or in Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the runtime dependency:

```bash
python -m pip install -r requirements.txt
```

### Run the desktop application

```bash
python run_desktop.py
```

### Run the terminal application

```bash
python main.py
```

The terminal handles one operation per launch.

## Testing

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

The test suite covers the domain model, storage, both interfaces, and application startup.

## Behavior and Limitations

### Data

- Sessions are stored in `data/sessions.json`.
- The file and directory are created on the first save.
- The path is resolved from the project directory.
- The file is excluded from Git because it contains local notes.
- Storage is local: no database, cloud sync, accounts, or encryption.
- Do not write from desktop and terminal instances at the same time; there is no file locking, so one instance can overwrite another instance's changes.
- If the sessions file exists, it must contain a JSON array of valid session records or startup will fail.

Each save is written to `sessions.json.tmp` and applied with `os.replace()`. A `finally` block removes leftover temporary files. The previous JSON remains intact if writing or replacement fails.

### Session Rules

- Notes are trimmed and cannot be empty.
- Dates must be real, non-future dates in `YYYY-MM-DD` format.
- Session numbers continue from the highest stored number.
- Archived sessions remain stored but cannot be searched or updated.
- Archived numbers are never reused.
- Keyword searches are case-insensitive substring matches.
- Desktop settings are stored only in memory and reset after restart.

## Architecture

```text
session-notes/
├── backend/
│   ├── coding_session.py   # Session model, validation, and serialization
│   ├── session_tracker.py  # Collection, numbering, search, update, archive
│   └── json_storage.py     # JSON loading and atomic persistence
├── frontend/
│   ├── desktop_ui.py       # PySide6 widget, dialogs, tray, and settings
│   ├── terminal_ui.py      # Terminal menus and input/output
│   └── styles.py           # Qt dark and light stylesheets
├── tests/                  # Backend, UI, storage, and startup tests
├── app_setup.py            # Shared dependency construction and data path
├── main.py                 # Terminal entry point
└── run_desktop.py          # Desktop entry point
```

The domain model, collection logic, persistence, and presentation are separate. `app_setup.py` constructs and connects the tracker and storage for either entry point. Both frontends reuse the same backend.

## One-Month Learning Summary

- **OOP:** Built `CodingSession` and `SessionTracker` with clear responsibilities and custom exceptions.
- **Architecture:** Shared one backend between terminal and desktop through injected dependencies.
- **JSON persistence:** Added serialization, UTF-8 storage, directory creation, atomic replacement, and temporary-file cleanup.
- **PySide6:** Used widgets, layouts, signals, dialogs, tray actions, window flags, themes, and lifecycle events.
- **UI workflows:** Built combined search, result selection, updates, archiving, and back navigation.
- **Validation:** Enforced non-empty notes, strict dates, stable numbering, and archive rules.
- **Testing:** Used fixtures, parametrization, temporary paths, monkeypatching, fakes, captured output, and Qt widget tests.
- **Agentic coding:** Practiced planning, prompting, reviewing, and iterating with a coding agent.
