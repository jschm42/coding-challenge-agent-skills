---
name: generate-python-exercise-project
description: >-
  Use this skill when the user asks to generate a new interactive Python coding challenge, exercise project, or executable learning application (e.g. calculator, CLI tool, or mini-app). It creates a complete project based on the "Python Challenge" schema, including a Poetry configuration with separate scripts for the learning app and the Rich TUI dashboard, reference solutions (solutions.md), setup scripts, stubs with unit tests, and a README.
---

# Generate Python Challenge & Exercise Project

This skill instructs you how to generate a new Python coding practice project based on a modern, interactive schema featuring a [Rich](https://github.com/Textualize/rich) TUI dashboard, automatic test parsing, Poetry integration, and reference solutions. You can use this skill in any repository, even empty ones.

## Supported Project Modes

The skill supports two project types:

1. **Executable Application Challenge (e.g., Calculator, CLI Tool, Mini-Game)**:
   - The user builds a runnable application step by step.
   - The executable application file is named **`app.py`** (with `main()` entrypoint, interactive CLI/loop, and modular function/class stubs).
   - The interactive Rich TUI challenge runner is named **`tui.py`**.
   - Scripts in `pyproject.toml`:
     - `poetry run app`: Launches the student's executable application (`app.py`).
     - `poetry run tui`: Launches the interactive Rich TUI dashboard (`tui.py`).
     - `poetry run test`: Runs the automated test suite with diagnostic parsing (`tui:run_tests_cli`).

2. **Exercise Collection (e.g., Dictionaries, List Comprehensions, Decorators, OOP)**:
   - The user solves modular function exercises.
   - Stubs are placed in **`exercises.py`**.
   - Tests are in **`test_exercises.py`**.
   - The interactive Rich TUI challenge runner is named **`tui.py`** (`poetry run tui`).

> **CRITICAL NAMING RULE**: The TUI dashboard is **always named `tui.py`** (never `app.py`). The name `app.py` is reserved exclusively for the executable learning application!

## Schema Overview

A complete challenge project consists of 7 core files:
1. **`app.py`** (or `exercises.py`):
   - For App Challenges: An executable application file with `main()`, interactive command loop/CLI, and modular function/method stubs ending with `raise NotImplementedError(...)`.
   - For Exercise Collections: Stubs with type hints and docstrings grouped into logical categories.
2. **`test_app.py`** (or `test_exercises.py`): A `unittest.TestCase` suite testing each function or method covering standard and edge cases.
3. **`solutions.md`**: Reference solutions with complete working implementations, type hints, and explanations for each task.
4. **`pyproject.toml`**: Minimal PEP 621 Poetry config with `rich` dependency and scripts (`app`, `tui`, `challenge`, `test`).
5. **`setup.bat` & `setup.sh`**: Automated setup scripts that run `poetry install` (with graceful pip fallback).
6. **`tui.py`**: An interactive [Rich](https://github.com/Textualize/rich) TUI dashboard that runs the tests, parses test errors with exact locations/reasons, shows progress bars, and inspects code.
7. **`README.md`**: Project documentation and quickstart guide with Poetry and Python commands.

## Templates

The skill provides ready-to-use templates in the `templates/` folder:
- `[templates/tui_template.py](./templates/tui_template.py)`: Complete Rich TUI dashboard with test result parsing, task inspection, hints, and solution viewer.
- `[templates/app_template.py](./templates/app_template.py)`: Starter template for an executable CLI application with interactive REPL loop and `main()` entrypoint.
- `[templates/pyproject_template.toml](./templates/pyproject_template.toml)`: Minimal PEP 621 Poetry config with `rich` dependency and scripts (`app`, `tui`, `test`).
- `[templates/setup_template.bat](./templates/setup_template.bat)`: Windows setup script.
- `[templates/setup_template.sh](./templates/setup_template.sh)`: Linux/macOS setup script.

## Steps to Generate a New Project

When the user requests a new challenge project (e.g., "Build a Calculator CLI app" or "Python Dictionary Challenge"):

1. **Determine Mode, Scope, and Difficulty**:
   - Identify whether the user wants an **Executable Application Challenge** (e.g., Calculator, Todo CLI, Text Adventure, Unit Converter) or an **Exercise Collection** (e.g., Dictionaries, Decorators).
   - If NOT specified or ambiguous, **ask the user** for their preference:
     - Project type: Executable App (runnable application in `app.py`) vs. Exercise Collection (`exercises.py`)?
     - Number of tasks/milestones (default: 6-10 for apps, 10-15 for exercise sets) and difficulty level.

2. **Create Project Directory**:
   - Ask the user where to create the project or default to a sibling directory of the current one, or the current directory if it's an empty project.

3. **Generate `app.py` or `exercises.py`**:
   - Include type hints (`from typing import ...`).
   - Write clear docstrings with examples in **English** (unless the user explicitly requests another language).
   - For **Executable Apps (`app.py`)**:
     - Provide an interactive `main()` function with a REPL loop or CLI command parser.
     - Gracefully catch `NotImplementedError` in the CLI loop and inform the learner to implement the task or run `poetry run tui`.
     - End each function/method stub with:
       ```python
       # TODO: Task X - <Short Description in English>
       raise NotImplementedError("Task X not implemented yet!")
       ```
   - For **Exercise Collections (`exercises.py`)**:
     - Follow the standard stub schema with `NotImplementedError`.

4. **Generate Unit Tests (`test_app.py` or `test_exercises.py`)**:
   - Import `unittest` and all target functions/classes.
   - Create a class inheriting from `unittest.TestCase` (e.g., `TestCalculatorApp`).
   - Write robust tests for every function, checking both standard cases and edge cases. Name the tests `test_01_...`, `test_02_...`, etc.

5. **Generate `solutions.md`**:
   - Provide complete, clean, idiomatic reference solutions for all tasks/milestones.
   - Group them by category and task ID.
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
     app = "app:main"
     tui = "tui:main"
     challenge = "tui:main"
     test = "tui:run_tests_cli"

     [tool.poetry]
     packages = [{ include = "*.py" }]

     [build-system]
     requires = ["poetry-core"]
     build-backend = "poetry.core.masonry.api"
     ```

7. **Generate `setup.bat` & `setup.sh`**:
   - Copy `[setup_template.bat](./templates/setup_template.bat)` and `[setup_template.sh](./templates/setup_template.sh)`.
   - These scripts automatically check for Poetry, run `poetry install`, and fall back to `pip install rich` if needed.

8. **Generate `tui.py`**:
   - Use `[tui_template.py](./templates/tui_template.py)` as the foundation.
   - Configure `PROJECT_TITLE`, `PROJECT_SUBTITLE`, and an engaging `PROJECT_INTRO` displayed in the dashboard banner.
   - Set `TARGET_MODULE` to `"app"` (for executable apps) or `"exercises"` (for exercise sets).
   - Update the `TASKS` list in `tui.py` to match the tasks, including progressive solution `hints` for each task:
     ```python
     TASKS = [
         {
             "id": 1,
             "test": "test_01_add",
             "name": "add",
             "title": "Implement basic addition",
             "category": "Basic Operations",
             "hints": [
                 "Inspect the function arguments in app.py.",
                 "Return the sum of a and b as float.",
             ],
         },
         ...
     ]
     ```
   - Ensure `tui.py` includes:
     - Test execution parsing (`ParsedTestResult`) to catch `NotImplementedError` as `NOT_IMPLEMENTED` and errors with exact locations/reasons.
     - Solution hints viewer (`--hint <id>` and menu option 4).
     - Direct reference solution extraction from `solutions.md` (`--solution <id>` and menu option 5).
     - If `app.py` is present, menu option 7 to run the application directly from the TUI.

9. **Generate `README.md`**:
   - Include project title and description.
   - Quickstart commands:
     - Run TUI Dashboard: `poetry run tui` (or `python tui.py`)
     - Run Learning Application: `poetry run app` (or `python app.py`)
     - Run Tests: `poetry run test` (or `python tui.py --test`)
   - Fast commands table (`python tui.py --check`, `python tui.py --task <id>`, `python tui.py --hint <id>`, `python tui.py --solution <id>`).
   - Overview of the tasks/milestones grouped by category.

10. **Verify Installation & Execution**:
    - Run `poetry install` or verify dependency setup.
    - Run `python tui.py --check` or `poetry run test` to verify that all tests load and properly report pending status (`○ PENDING`).
    - If in executable app mode, test `python app.py` (or `poetry run app`) to verify the CLI loop or entry point starts cleanly.

## Constraints
- **ALL GENERATED TEXT, DOCSTRINGS, TERMINAL OUTPUTS, AND COMMENTS MUST BE IN ENGLISH** (unless explicitly requested otherwise by the user).
- **Naming Convention**: The TUI dashboard file MUST be named `tui.py`. The executable app MUST be named `app.py`. Never name the TUI `app.py`.
- **Poetry Integration**: Always provide `pyproject.toml` with `[project.scripts]` defining `app = "app:main"`, `tui = "tui:main"`, and `test = "tui:run_tests_cli"`.
- **Rich TUI**: Use [Rich](https://github.com/Textualize/rich) for formatted tables, panels, syntax highlighting, and progress bars.
- **Test Parsing**: Do not scrape raw stdout; use `unittest.TestResult` callbacks to accurately extract exception types, assertion messages, filenames, and line numbers.
- **Reference Solutions**: Always generate `solutions.md` with complete implementations alongside the exercise/app stubs.
- **Windows Console**: Always configure UTF-8 output (`sys.stdout.reconfigure(encoding="utf-8")`) to avoid `charmap` encoding errors with Unicode symbols.
