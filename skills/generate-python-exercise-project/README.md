# 🐍 Python Challenge & App Generator (`generate-python-exercise-project`)

An agentic skill that automatically generates complete, interactive, test-driven Python coding challenge projects and executable learning applications featuring a [Rich](https://github.com/Textualize/rich) TUI dashboard, progressive test diagnostics, automated setup scripts, reference solutions, and Clean Code architecture (`/app` and `/test` folders).

---

## 🚀 How to Use

Invoke this skill in Antigravity or any compatible agent by prompting or using the slash command:

```text
/generate-python-exercise-project Build an interactive calculator application challenge with 6 tasks
```

Or simply ask naturally:
> *"Create an interactive Python challenge for a calculator app with clean code structure in /app and tests in /test."*
> *"Generate an interactive Python challenge on list comprehension with 10 exercises."*

---

## 📦 Clean Code Project Structure

### 1. Dedicated `/app` & `/test` Subdirectories
- **`/app` Package**: All learning application source code resides in the `app/` directory (`app/__init__.py`, `app/main.py`).
  - For complex projects, domain logic is modularized across multiple files according to Clean Code principles (e.g., `app/operations.py`, `app/models.py`, `app/parser.py`).
- **`/test` Directory**: All automated unit tests reside in the `test/` directory (`test/__init__.py`).
  - Tests can be split across multiple test files matching domain modules (e.g., `test/test_operations.py`, `test/test_parser.py`) or in a unified `test/test_app.py`.
- **`tui.py` Dashboard**: Rich TUI challenge runner at the project root (`poetry run tui`). Automatically discovers tests in `/test` and inspects symbols across all `/app` modules.

### Project Layout
```text
<project-root>/
├── app/                        # Learning application package
│   ├── __init__.py             # Package marker & public exports
│   ├── main.py                 # Application entry point with CLI / REPL loop & main()
│   ├── <module1>.py            # Domain logic stubs (e.g. operations.py)
│   └── <module2>.py            # (Optional) additional domain files (e.g. models.py)
├── test/                       # Unit test suite directory
│   ├── __init__.py             # Test package marker
│   ├── test_<module1>.py       # Modular tests for module1
│   └── test_<module2>.py       # (Optional) additional modular test files
├── tui.py                      # Interactive Rich TUI dashboard & test runner
├── solutions.md                # Comprehensive reference solutions & explanations
├── pyproject.toml              # Modern Poetry configuration (PEP 621)
├── setup.bat / setup.sh        # Quick setup scripts (Poetry install + rich fallback)
└── README.md                   # Project documentation & quickstart
```

---

## 🖥️ Interactive Rich TUI Dashboard

![Interactive Rich TUI Dashboard](../../assets/tui_dashboard.svg)

---

## 🛠️ CLI & Poetry Commands

| Action | Poetry Command | Direct Python Command |
| :--- | :--- | :--- |
| **Run Executable App** | `poetry run app` | `python -m app.main` |
| **Launch TUI Dashboard** | `poetry run tui` | `python tui.py` |
| **Run All Tests** | `poetry run test` | `python tui.py --test` |
| **Quick Progress Check** | `poetry run tui --check` | `python tui.py --check` |
| **Inspect Specific Task** | `python tui.py --task <id>` | `python tui.py --task <id>` |
| **View Solution Hints** | `python tui.py --hint <id>` | `python tui.py --hint <id>` |
| **View Reference Solution** | `python tui.py --solution <id>` | `python tui.py --solution <id>` |

---

## 📂 Included Templates

The skill comes pre-packaged with robust templates in `templates/`:
- `templates/tui_template.py`: The complete Rich TUI engine with multi-file test discovery, task inspection across `/app` modules, hints, and reference solution viewer.
- `templates/app_template.py`: Starter template for an executable CLI application (`app/main.py`) with interactive REPL loop and `main()` entrypoint.
- `templates/pyproject_template.toml`: Configured Poetry project file defining `app` (`app.main:main`), `tui`, and `test` scripts.
- `templates/setup_template.bat`: Windows setup script.
- `templates/setup_template.sh`: Unix/macOS setup script.

