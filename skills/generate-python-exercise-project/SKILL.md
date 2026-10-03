---
name: generate-python-exercise-project
description: >-
  Use this skill when the user asks to generate a new interactive Python coding challenge, exercise project, or executable learning application (e.g. calculator, CLI tool, or mini-app). It creates a complete project based on the "Python Challenge" schema, including a dedicated /app package for the learning application (with multi-file Clean Code support), a /test directory for modular unit tests, a Poetry configuration with separate scripts, reference solutions (solutions.md), setup scripts, Rich TUI dashboard, and a README.
---

# Generate Python Challenge & Exercise Project

This skill instructs you how to generate a new Python coding practice project based on a modern, interactive schema featuring a [Rich](https://github.com/Textualize/rich) TUI dashboard, automatic test parsing, Poetry integration, Clean Code architecture with dedicated `/app` and `/test` folders, and reference solutions. You can use this skill in any repository, even empty ones.

## Supported Project Modes

The skill supports two project types:

1. **Executable Application Challenge (e.g., Calculator, CLI Tool, Mini-Game)**:
   - The user builds a runnable application step by step.
   - All learning application files reside in the **`app/`** subfolder (as an importable Python package with `app/__init__.py`, `app/main.py`, and optional modular domain files).
   - All unit test files reside in the **`test/`** subfolder (with `test/__init__.py` and one or more modular test files).
   - The interactive Rich TUI challenge runner is named **`tui.py`** (at project root).
   - Scripts in `pyproject.toml`:
     - `poetry run app`: Launches the student's executable application (`app.main:main`).
     - `poetry run tui`: Launches the interactive Rich TUI dashboard (`tui.py`).
     - `poetry run test`: Runs the automated test suite with diagnostic parsing (`tui:run_tests_cli`).

2. **Exercise Collection (e.g., Dictionaries, List Comprehensions, Decorators, OOP)**:
   - The user solves modular function exercises.
   - Files are placed in **`app/`** (or `exercises/`) and tests in **`test/`** (e.g. `test/test_exercises.py`).
   - The interactive Rich TUI challenge runner is named **`tui.py`** (`poetry run tui`).

> **CRITICAL ARCHITECTURE RULES**:
> 1. All learning application source files MUST go into the **`/app`** directory (never scattered across the root).
> 2. All unit test files MUST go into the **`/test`** directory.
> 3. The TUI dashboard runner is **always named `tui.py` at the project root** (never inside `app/` and never named `app.py`).

## Clean Code & Multi-File Architecture

To keep exercise projects maintainable, readable, and extensible—especially as complexity grows—apply **Clean Code principles**:

### 1. Separation of Concerns (SoC) & Single Responsibility
Do NOT cram everything into a single monolithic 500-line file. Split the logic into distinct, focused modules:
- **`app/main.py`**: User interface, CLI arguments, interactive REPL loop, and catching `NotImplementedError` with friendly guidance.
- **`app/<domain>.py`** (e.g., `operations.py`, `calculator.py`, `parser.py`, `engine.py`): Pure functions, domain logic, and core algorithms.
- **`app/models.py`** (if applicable): Data classes, state representations, or enum types.
- **`app/__init__.py`**: Exposes primary package functions and marks `app` as an importable package.

### 2. Modular Test Suites in `/test`
Mirror the application modules in `/test` to keep tests organized:
- **`test/test_operations.py`**: Unit tests for arithmetic or core operations (`TestOperations`).
- **`test/test_parser.py`**: Unit tests for expression parsing and validation (`TestParser`).
- **`test/test_main.py`**: Tests for the CLI or REPL commands (`TestMainCLI`).
- Or for smaller projects: `test/test_app.py` covering all tasks.

### 3. Complexity Guidelines:
- **Simple Challenge (< 5 tasks)**: Can use `app/main.py` (with helper functions) and `test/test_app.py`.
- **Intermediate / Complex Challenge (6+ tasks, stateful apps, multi-feature tools)**: **Always create multiple files in `app/` and multiple test files in `test/`**. This makes it vastly easier for the learner to stay oriented and follow Clean Code practices.

## Schema Overview

A complete challenge project is structured as follows:

```text
<project-root>/
├── app/                        # Learning application package (Clean Code)
│   ├── __init__.py             # Package marker & public exports
│   ├── main.py                 # Application entry point with CLI / REPL loop & main()
│   ├── <module1>.py            # Domain logic stubs (e.g. operations.py)
│   └── <module2>.py            # (Optional) additional domain files (e.g. models.py, parser.py)
├── test/                       # Unit test suite directory
│   ├── __init__.py             # Test package marker
│   ├── test_<module1>.py       # Modular tests for module1
│   └── test_<module2>.py       # (Optional) additional modular test files
├── tui.py                      # Interactive Rich TUI dashboard & diagnostic test runner
├── solutions.md                # Comprehensive reference solutions & explanations
├── pyproject.toml              # Modern Poetry configuration (PEP 621)
├── setup.bat                   # Windows automated setup script
├── setup.sh                    # Linux/macOS automated setup script
└── README.md                   # Project documentation & quickstart
```

### Core File Roles:
1. **`app/` package**: Contains `__init__.py`, `main.py`, and domain modules. Function/method stubs end with `raise NotImplementedError(...)`.
2. **`test/` directory**: Contains `unittest.TestCase` suites testing each module covering standard and edge cases.
3. **`solutions.md`**: Reference solutions with complete working implementations, type hints, and explanations for each task.
4. **`pyproject.toml`**: Minimal PEP 621 Poetry config with `rich` dependency, `packages = [{ include = "app" }]`, and scripts (`app`, `tui`, `challenge`, `test`).
5. **`setup.bat` & `setup.sh`**: Automated setup scripts that run `poetry install` (with graceful pip fallback).
6. **`tui.py`**: Interactive [Rich](https://github.com/Textualize/rich) TUI dashboard that auto-discovers tests in `test/`, parses errors with exact locations/reasons, shows progress bars, and inspects code.
7. **`README.md`**: Project documentation and quickstart guide with Poetry and Python commands.

## Templates

The skill provides ready-to-use templates in the `templates/` folder:
- `[templates/tui_template.py](./templates/tui_template.py)`: Complete Rich TUI dashboard with multi-file test discovery, task inspection across modules in `app/`, hints, and solution viewer.
- `[templates/app_template.py](./templates/app_template.py)`: Starter template for executable CLI application (`app/main.py`) with interactive REPL loop and `main()` entrypoint.
- `[templates/pyproject_template.toml](./templates/pyproject_template.toml)`: Minimal PEP 621 Poetry config with `rich` dependency, `app` package inclusion, and scripts (`app`, `tui`, `test`).
- `[templates/setup_template.bat](./templates/setup_template.bat)`: Windows setup script.
- `[templates/setup_template.sh](./templates/setup_template.sh)`: Linux/macOS setup script.

## Steps to Generate a New Project

When the user requests a new challenge project (e.g., "Build a Calculator CLI app" or "Python Dictionary Challenge"):

1. **Determine Mode, Scope, and Architecture**:
   - Identify whether the user wants an **Executable Application Challenge** or an **Exercise Collection**.
   - If NOT specified or ambiguous, **ask the user** for their preference:
     - Project type: Executable App (runnable application in `app/`) vs. Exercise Collection?
     - Number of tasks/milestones (default: 6-10 for apps, 10-15 for exercise sets) and difficulty level.
   - For complex apps, plan a **multi-file modular architecture** in `app/` and `test/` upfront (e.g. `app/operations.py`, `app/parser.py`, `app/main.py`).

2. **Create Project Directory Structure**:
   - Create root folder, `app/`, and `test/` directories.
   - Add empty `app/__init__.py` and `test/__init__.py`.

3. **Generate Application Modules in `app/`**:
   - Include type hints (`from typing import ...`).
   - Write clear docstrings with examples in **English** (unless the user explicitly requests another language).
   - Use Clean Code modularization (e.g. `app/operations.py`, `app/parser.py`, `app/main.py`).
   - In `app/main.py`:
     - Provide an interactive `main()` function with a REPL loop or CLI command parser.
     - Gracefully catch `NotImplementedError` in the CLI loop and inform the learner to implement the task or run `poetry run tui`.
   - End each function/method stub with:
     ```python
     # TODO: Task X - <Short Description in English>
     raise NotImplementedError("Task X not implemented yet!")
     ```

4. **Generate Unit Tests in `test/`**:
   - Mirror application modules (e.g. `test/test_operations.py`, `test/test_parser.py`, or `test/test_app.py`).
   - Import `unittest` and all target functions/classes using package imports (e.g., `from app.operations import add`).
   - Create classes inheriting from `unittest.TestCase` (e.g., `TestOperations`, `TestParser`).
   - Write robust tests for every function, checking both standard cases and edge cases. Name tests `test_01_...`, `test_02_...`, etc.

5. **Generate `solutions.md`**:
   - Provide complete, clean, idiomatic reference solutions for all tasks/milestones.
   - Group them by module, category, and task ID.
   - Include code blocks with type hints and concise explanations of the approach, time/space complexity, or Pythonic idioms used.

6. **Generate `pyproject.toml`**:
   - Use `[pyproject_template.toml](./templates/pyproject_template.toml)` as reference.
   - Use modern PEP 621 format with `package-mode = false`:
     ```toml
     [project]
     name = "<project-name>"
     version = "0.1.0"
     description = "<Project Description>"
     authors = [{ name = "Learner" }]
     readme = "README.md"
     requires-python = ">=3.10"
     dependencies = [
         "rich>=13.7.0",
     ]

     [project.scripts]
     app = "app.main:main"
     tui = "tui:main"
     challenge = "tui:main"
     test = "tui:run_tests_cli"

     [tool.poetry]
     packages = [{ include = "app" }]

     [build-system]
     requires = ["poetry-core"]
     build-backend = "poetry.core.masonry.api"
     ```

7. **Generate `setup.bat` & `setup.sh`**:
   - Copy `[setup_template.bat](./templates/setup_template.bat)` and `[setup_template.sh](./templates/setup_template.sh)`.
   - These scripts automatically check for Poetry, run `poetry install`, and fall back to `pip install rich` if needed.

8. **Generate `tui.py`**:
   - Use `[tui_template.py](./templates/tui_template.py)` as the foundation at the project root.
   - Configure `PROJECT_TITLE`, `PROJECT_SUBTITLE`, and an engaging `PROJECT_INTRO`.
   - Populate `TASKS` list in `tui.py` matching the tasks across all modules, including progressive solution `hints`:
     ```python
     TASKS = [
         {
             "id": 1,
             "test": "test_01_add",
             "name": "add",
             "title": "Implement basic addition",
             "category": "Basic Operations",
             "hints": [
                 "Inspect the function arguments in app/operations.py.",
                 "Return the sum of a and b as float.",
             ],
         },
         ...
     ]
     ```
   - Ensure `tui.py` includes:
     - Automated test discovery across all test files in `test/`.
     - Multi-module target inspection in `app/`.
     - Solution hints viewer (`--hint <id>` and menu option 4).
     - Direct reference solution extraction from `solutions.md` (`--solution <id>` and menu option 5).
     - Menu option 7 to run the application directly from the TUI (`poetry run app`).

9. **Generate `README.md`**:
   - Include project title, architecture overview, and quickstart commands:
     - Run TUI Dashboard: `poetry run tui` (or `python tui.py`)
     - Run Learning Application: `poetry run app` (or `python -m app.main`)
     - Run Tests: `poetry run test` (or `python tui.py --test`)
   - Fast commands table (`python tui.py --check`, `python tui.py --task <id>`, `python tui.py --hint <id>`, `python tui.py --solution <id>`).
   - Overview of the tasks/milestones grouped by module/category.

10. **Verify Installation & Execution**:
    - Run `poetry install` or verify dependency setup.
    - Run `python tui.py --check` or `poetry run test` to verify that all tests in `test/` load and properly report pending status (`○ NOT IMPLEMENTED`).
    - Test `poetry run app` (or `python -m app.main`) to verify the CLI loop or entry point starts cleanly.

## Constraints
- **ALL GENERATED TEXT, DOCSTRINGS, TERMINAL OUTPUTS, AND COMMENTS MUST BE IN ENGLISH** (unless explicitly requested otherwise by the user).
- **Directory Structure**:
  - Application code MUST reside in `/app`.
  - Unit tests MUST reside in `/test`.
  - TUI dashboard MUST reside in project root as `tui.py`.
- **Clean Code & Separation of Concerns**: For non-trivial apps, split code into multiple logical modules in `/app` and modular test files in `/test`.
- **Poetry Integration**: Always provide `pyproject.toml` with `app = "app.main:main"`, `tui = "tui:main"`, `test = "tui:run_tests_cli"`, and `packages = [{ include = "app" }]`.
- **Rich TUI**: Use [Rich](https://github.com/Textualize/rich) for formatted tables, panels, syntax highlighting, and progress bars.
- **Test Parsing**: Do not scrape raw stdout; use `unittest.TestResult` callbacks to accurately extract exception types, assertion messages, filenames, and line numbers.
- **Reference Solutions**: Always generate `solutions.md` with complete implementations alongside the exercise/app stubs.
- **Windows Console**: Always configure UTF-8 output (`sys.stdout.reconfigure(encoding="utf-8")`) to avoid `charmap` encoding errors with Unicode symbols.

