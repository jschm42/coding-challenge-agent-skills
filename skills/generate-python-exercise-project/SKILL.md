---
name: generate-python-exercise-project
description: >-
  Use this skill when the user asks to generate a new interactive Python coding challenge or exercise project. It creates a complete project based on the "Python Challenge" schema, including a Poetry configuration, Rich TUI dashboard with test parsing, reference solutions (solutions.md), setup scripts, exercise stubs, unit tests, and a README.
---

# Generate Exercise Project

This skill instructs you how to generate a new Python coding exercise project based on a modern, interactive schema featuring a [Rich](https://github.com/Textualize/rich) TUI, automatic test parsing, Poetry integration, and reference solutions. You can use this skill in any repository, even empty ones.

## Schema Overview

A standard exercise project consists of 7 core files:
1. `exercises.py`: Contains the function stubs with type hints, detailed docstrings, and `raise NotImplementedError(...)`. Grouped into logical categories.
2. `test_exercises.py`: A `unittest.TestCase` suite testing each function in `exercises.py` covering standard and edge cases.
3. `solutions.md`: Reference solutions with complete working implementations, type hints, and explanations for each task.
4. `pyproject.toml`: Minimal Poetry config with `rich` dependency and scripts (`poetry run app`, `poetry run test`).
5. `setup.bat` & `setup.sh`: Automated setup scripts that run `poetry install` (with graceful pip fallback).
6. `app.py`: An interactive [Rich](https://github.com/Textualize/rich) TUI dashboard that runs the tests, parses test errors with exact locations/reasons, shows progress bars, and inspects code.
7. `README.md`: Project documentation and quickstart guide with Poetry and Python commands.

## Templates

The skill provides ready-to-use templates in the `templates/` folder:
- `templates/pyproject_template.toml`: Minimal PEP 621 Poetry config with `rich` dependency and scripts.
- `templates/setup_template.bat`: Windows setup script.
- `templates/setup_template.sh`: Linux/macOS setup script.
- `templates/app_template.py`: Complete Rich TUI dashboard with test result parsing and task inspection.

## Steps to Generate a New Project

When the user requests a new exercise project (e.g., "Python Dictionary Challenge"):

1. **Determine Topic, Scope, and Difficulty**:
   - Check if the user specified the number of exercises and the desired difficulty level.
   - If NOT specified, **ask the user** for their preferences before proceeding (e.g., "How many exercises would you like? What should the difficulty level be?").
   - Identify the core topic (e.g., Dictionaries, Sets, OOP, List Handling).
   - Plan the requested number of exercises (or default to 10-15) divided into 3-4 logical categories (e.g., Basics, Intermediate, Advanced, Transformation) matching the requested difficulty.

2. **Create Project Directory**:
   - Ask the user where to create the project or default to a sibling directory of the current one, or the current directory if it's an empty project.

3. **Generate `exercises.py`**:
   - Include type hints (`from typing import ...`).
   - Write clear docstrings with examples in **English** (unless the user explicitly requests another language).
   - End each function with:
     ```python
     # TODO: Task X - <Short Description in English>
     raise NotImplementedError("Task X not implemented yet!")
     ```

4. **Generate `test_exercises.py`**:
   - Import `unittest` and all functions from `exercises.py`.
   - Create a class inheriting from `unittest.TestCase` (e.g., `TestDictionaryExercises`).
   - Write robust tests for every function, checking both standard cases and edge cases. Name the tests `test_01_...`, `test_02_...`, etc.

5. **Generate `solutions.md`**:
   - Provide complete, clean, idiomatic reference solutions for all tasks.
   - Group them by category and task ID matching `exercises.py`.
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
     test = "app:run_tests_cli"

     [tool.poetry]
     packages = [{ include = "app.py" }, { include = "exercises.py" }]

     [build-system]
     requires = ["poetry-core"]
     build-backend = "poetry.core.masonry.api"
     ```

7. **Generate `setup.bat` & `setup.sh`**:
   - Copy `[setup_template.bat](./templates/setup_template.bat)` and `[setup_template.sh](./templates/setup_template.sh)`.
   - These scripts automatically check for Poetry, run `poetry install`, and fall back to `pip install rich` if needed.

8. **Generate `app.py`**:
   - Use `[app_template.py](./templates/app_template.py)` as the foundation.
   - Configure `PROJECT_TITLE`, `PROJECT_SUBTITLE`, and an engaging `PROJECT_INTRO` introduction text displayed in the dashboard banner.
   - Update the `TASKS` list in `app.py` to match the exercises, including progressive solution `hints` for each task:
     ```python
     TASKS = [
         {
             "id": 1,
             "test": "test_01_add_element",
             "name": "add_element",
             "title": "Add an element to the end",
             "category": "Basics",
             "hints": [
                 "Inspect the function arguments and return type in exercises.py.",
                 "Use the append() method on list objects.",
                 "Remember to return the modified list.",
             ],
         },
         ...
     ]
     ```
   - Ensure `app.py` includes:
     - Test execution parsing (`ParsedTestResult`) to catch `NotImplementedError` as `NOT_IMPLEMENTED` and errors with exact locations/reasons.
     - Solution hints viewer (`--hint <id>` and menu option 4).
     - Direct reference solution extraction from `solutions.md` with syntax highlighting and explanation rendering (`--solution <id>` and menu option 5).

9. **Generate `README.md`**:
   - Include title, quickstart with Poetry (`poetry install && poetry run app`) and setup scripts (`setup.bat` / `setup.sh`), fast commands table (`poetry run test`, `poetry run app --check`, `python app.py --task <id>`), and an overview of the tasks grouped by category.

10. **Verify Installation & Execution**:
    - Run `poetry install` or verify dependency setup.
    - Run `python app.py --check` or `poetry run test` to verify that all tests load and properly report pending status (`○ PENDING`).

## Constraints
- **ALL GENERATED TEXT, DOCSTRINGS, TERMINAL OUTPUTS, AND COMMENTS MUST BE IN ENGLISH** (unless explicitly requested otherwise by the user).
- **Poetry Integration**: Always provide `pyproject.toml` with `packages` inclusion and `[project.scripts]` defining `app` and `test`.
- **Rich TUI**: Use [Rich](https://github.com/Textualize/rich) for formatted tables, panels, syntax highlighting, and progress bars.
- **Test Parsing**: Do not scrape raw stdout; use `unittest.TestResult` callbacks to accurately extract exception types, assertion messages, filenames, and line numbers.
- **Reference Solutions**: Always generate `solutions.md` with complete implementations alongside the exercise stubs.
- **Windows Console**: Always configure UTF-8 output (`sys.stdout.reconfigure(encoding="utf-8")`) to avoid `charmap` encoding errors with Unicode symbols.
