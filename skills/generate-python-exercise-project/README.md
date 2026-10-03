# 🐍 Python Exercise Project Generator (`generate-python-exercise-project`)

An agentic skill that automatically generates complete, interactive, test-driven Python coding challenge projects featuring a [Rich](https://github.com/Textualize/rich) TUI dashboard, progressive test diagnostics, automated setup scripts, and reference solutions.

---

## 🚀 How to Use

Invoke this skill in Antigravity or any compatible agent by prompting or using the slash command:

```text
/generate-python-exercise-project Create a beginner challenge on Python dictionaries with 8 exercises
```

Or simply ask naturally:
> *"Create an interactive Python challenge on list comprehension with 10 exercises."*

---

## 📦 What It Generates

Each generated exercise project follows a production-grade 7-file schema:

1. **`exercises.py`**: Function stubs with complete type hints, clear English docstrings, usage examples, and `NotImplementedError` stubs.
2. **`test_exercises.py`**: A comprehensive `unittest.TestCase` suite testing standard behavior and edge cases.
3. **`solutions.md`**: Full reference solutions with type annotations, idiomatic explanations, and algorithmic complexity notes.
4. **`pyproject.toml`**: Modern PEP 621 Poetry configuration specifying `rich` and CLI scripts (`poetry run app`, `poetry run test`).
5. **`setup.bat` & `setup.sh`**: Cross-platform one-step environment setup (Poetry with graceful pip fallback).
6. **`app.py`**: Rich TUI interactive terminal application featuring:
   - Live progress bars and task tables
   - Test execution with parsed diagnostic tracebacks
   - Progressive hints per task
   - Reference solution viewer directly within terminal
   - Interactive CLI menu & flags (`--check`, `--test`, `--task <id>`, `--hint <id>`, `--solution <id>`)
7. **`README.md`**: Student-facing documentation with quickstart guides and command references.

---

## 📂 Included Templates

The skill comes pre-packaged with robust templates in `templates/`:
- `templates/app_template.py`: The complete Rich TUI engine with unittest result interception.
- `templates/pyproject_template.toml`: Configured Poetry project file.
- `templates/setup_template.bat`: Windows setup script.
- `templates/setup_template.sh`: Unix/macOS setup script.
