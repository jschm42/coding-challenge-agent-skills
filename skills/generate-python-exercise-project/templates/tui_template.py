#!/usr/bin/env python3
"""
Interactive Python Coding Challenge TUI Dashboard
=================================================
Powered by Rich TUI & Unittest Result Parsing

Usage:
    poetry run tui              # Interactive challenge dashboard & menu
    poetry run app              # Run the executable learning app (if applicable)
    poetry run test             # Run all tests directly
or:
    python tui.py               # Interactive menu
    python tui.py --check       # Quick dashboard check (exit code 0 if all passed)
    python tui.py --test        # Detailed test runner
    python tui.py --task <id>   # Inspect specific task and current code
    python tui.py --hint <id>   # View extended hints for a specific task
    python tui.py --solution <id> # View reference solution for a specific task
    python tui.py --solutions   # Reference solutions overview
"""

import sys
import os
import re
import unittest
import inspect
import traceback
import time
from typing import Dict, List, Any, Optional

# Windows Console Encoding & ANSI Support
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.system("")

# Ensure project root, /app, and /test folders are on sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
for _sub in ("app", "test", "tests"):
    _p = os.path.join(ROOT_DIR, _sub)
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

# Rich Imports with Graceful Fallback
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich import box
except ImportError:
    print("\n[ERROR] The 'rich' library is required to run this dashboard.")
    print("Please set up your environment with:")
    print("    poetry install && poetry run tui")
    print("or:")
    print("    pip install rich\n")
    sys.exit(1)

console = Console()

# ==============================================================================
# PROJECT & TASK CONFIGURATION
# TODO: Agent should update this section when generating a new challenge project
# ==============================================================================
PROJECT_TITLE = "🐍 PYTHON CODING CHALLENGE 🐍"
PROJECT_SUBTITLE = "Master Python step by step with interactive tests & Rich TUI"
PROJECT_INTRO = (
    "Welcome to the Python Coding Challenge! This interactive training course helps "
    "you master core Python concepts with real-time test feedback and structured tasks.\n\n"
    "• Track your progress, inspect tasks, and get real-time feedback\n"
    "• Run tests via this dashboard or run your application directly\n"
    "• Stuck? View progressive hints or reference solutions directly from the menu!"
)

# Automatically identify primary source structure (app/ package, app.py, or exercises.py)
HAS_APP_DIR = os.path.isdir(os.path.join(ROOT_DIR, "app"))
HAS_TEST_DIR = os.path.isdir(os.path.join(ROOT_DIR, "test")) or os.path.isdir(os.path.join(ROOT_DIR, "tests"))

TARGET_MODULE = "app" if HAS_APP_DIR or os.path.exists("app.py") else "exercises"
TARGET_FILE = "app/main.py" if HAS_APP_DIR else f"{TARGET_MODULE}.py"


TASKS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "test": "test_01_example",
        "name": "example_func",
        "title": "Example Task",
        "category": "Basics",
        "hints": [
            "Inspect the function arguments and return type in the source file.",
            "Consider standard library functions or idioms for this task.",
            "Check edge cases such as empty inputs or unexpected types.",
        ],
    }
]


# ==============================================================================
# TEST RUNNER & RESULT PARSING
# ==============================================================================
class ParsedTestResult(unittest.TestResult):
    """Custom TestResult capturing detailed error types, messages, and code locations."""

    def __init__(self):
        super().__init__()
        self.status = "PASSED"  # "PASSED", "NOT_IMPLEMENTED", "FAILED"
        self.error_name = ""
        self.error_message = ""
        self.location = ""
        self.full_traceback = ""

    def addSuccess(self, test):
        super().addSuccess(test)
        self.status = "PASSED"

    def addError(self, test, err):
        super().addError(test, err)
        exctype, value, tb = err
        self.error_name = exctype.__name__
        self.error_message = str(value)
        self.full_traceback = "".join(traceback.format_exception(*err))
        if issubclass(exctype, NotImplementedError):
            self.status = "NOT_IMPLEMENTED"
            self.error_message = "Not implemented yet (raise NotImplementedError)"
        else:
            self.status = "FAILED"
        self._extract_location(tb)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        exctype, value, tb = err
        self.status = "FAILED"
        self.error_name = exctype.__name__
        self.error_message = str(value)
        self.full_traceback = "".join(traceback.format_exception(*err))
        self._extract_location(tb)

    def _extract_location(self, tb):
        frames = traceback.extract_tb(tb)
        for frame in reversed(frames):
            norm_path = os.path.abspath(frame.filename)
            if ROOT_DIR in norm_path:
                rel = os.path.relpath(norm_path, ROOT_DIR).replace("\\", "/")
                # Prefer project source files (in app/, test/, or root)
                if (
                    rel.startswith("app/")
                    or rel.startswith("test/")
                    or rel.startswith("tests/")
                    or rel in ("exercises.py", "app.py", "test_exercises.py", "test_app.py")
                ):
                    self.location = f"{rel}:{frame.lineno} in {frame.name}()"
                    return
        if frames:
            last = frames[-1]
            self.location = f"{os.path.basename(last.filename)}:{last.lineno} in {last.name}()"


def discover_test_modules() -> List[Any]:
    """Dynamically discover and import all test modules in test/, tests/, or current directory."""
    modules = []
    search_dirs = []
    for d in ("test", "tests", "."):
        path = os.path.join(ROOT_DIR, d)
        if os.path.isdir(path) and path not in search_dirs:
            search_dirs.append(path)

    import importlib.util
    for sdir in search_dirs:
        try:
            entries = sorted(os.listdir(sdir))
        except OSError:
            continue
        for fname in entries:
            if fname.endswith(".py") and (fname.startswith("test_") or fname.endswith("_test.py")):
                mod_name = fname[:-3]
                file_path = os.path.join(sdir, fname)
                try:
                    if mod_name in sys.modules:
                        modules.append(sys.modules[mod_name])
                    else:
                        spec = importlib.util.spec_from_file_location(mod_name, file_path)
                        if spec and spec.loader:
                            mod = importlib.util.module_from_spec(spec)
                            sys.modules[mod_name] = mod
                            spec.loader.exec_module(mod)
                            modules.append(mod)
                except Exception:
                    pass
    return modules


def get_all_test_case_classes() -> List[type]:
    """Retrieve all unittest.TestCase classes across all discovered test modules."""
    test_classes = []
    for mod in discover_test_modules():
        for _, obj in inspect.getmembers(mod, inspect.isclass):
            if issubclass(obj, unittest.TestCase) and obj is not unittest.TestCase:
                if obj not in test_classes:
                    test_classes.append(obj)
    return test_classes


def get_test_case_for_method(test_method_name: str) -> type:
    """Find the TestCase class that defines or includes the specified test method."""
    classes = get_all_test_case_classes()
    for cls in classes:
        if hasattr(cls, test_method_name):
            return cls
    if classes:
        return classes[0]
    raise RuntimeError("No unittest.TestCase subclass found in test/ directory or current directory.")


def run_single_test(test_method_name: str) -> dict:
    """Execute a single test method and parse detailed execution metrics and errors."""
    test_cls = get_test_case_for_method(test_method_name)
    suite = unittest.TestSuite()
    try:
        suite.addTest(test_cls(test_method_name))
    except Exception:
        suite.addTest(test_cls())

    result = ParsedTestResult()
    start_time = time.perf_counter()
    suite.run(result)
    duration_ms = (time.perf_counter() - start_time) * 1000

    return {
        "status": result.status,
        "error_name": result.error_name,
        "message": result.error_message,
        "location": result.location,
        "traceback": result.full_traceback,
        "duration_ms": duration_ms,
    }


def evaluate_all_tasks() -> List[dict]:
    """Evaluate all configured tasks and return parsed test outcomes."""
    results = []
    for task in TASKS:
        res = run_single_test(task["test"])
        results.append({**task, **res})
    return results


# ==============================================================================
# SOLUTIONS & HINTS PARSER
# ==============================================================================
def extract_task_solution(task_id: int) -> Optional[Dict[str, str]]:
    """Extract code implementation and explanation for a task directly from solutions.md."""
    if not os.path.exists("solutions.md"):
        return None
    try:
        with open("solutions.md", "r", encoding="utf-8") as f:
            content = f.read()

        pattern = rf"###\s+Task\s+{task_id}[:\s].*?(?=(?:\n###\s+Task|\Z))"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if not match:
            return None

        section = match.group(0)
        code_match = re.search(r"```python\s*(.*?)\s*```", section, re.DOTALL)
        code = code_match.group(1).strip() if code_match else ""

        exp_match = re.search(r"####\s+Explanation\s*(.*?)(?=\n###|\Z)", section, re.DOTALL)
        explanation = exp_match.group(1).strip() if exp_match else ""

        return {"code": code, "explanation": explanation, "raw": section}
    except Exception as e:
        return {"error": str(e), "code": "", "explanation": ""}


# ==============================================================================
# UI COMPONENTS (RICH TUI)
# ==============================================================================
def print_banner(include_intro: bool = True):
    """Display an eye-catching header panel with project branding and introduction."""
    lines = [
        f"[bold cyan]{PROJECT_TITLE}[/bold cyan]",
        f"[italic white]{PROJECT_SUBTITLE}[/italic white]\n",
    ]
    if include_intro and PROJECT_INTRO:
        lines.append(f"{PROJECT_INTRO}\n")

    if HAS_APP_DIR:
        lines.append(
            "[dim]Solve tasks in [/dim][bold yellow]app/[/bold yellow][dim] | "
            "Run app: [/dim][bold green]poetry run app[/bold green][dim] | "
            "Track progress: [/dim][bold cyan]poetry run tui[/bold cyan]"
        )
    elif os.path.exists("app.py"):
        lines.append(
            "[dim]Solve tasks in [/dim][bold yellow]app.py[/bold yellow][dim] | "
            "Run app: [/dim][bold green]poetry run app[/bold green][dim] | "
            "Track progress: [/dim][bold cyan]poetry run tui[/bold cyan]"
        )
    else:
        lines.append(
            f"[dim]Solve tasks in [/dim][bold yellow]{TARGET_FILE}[/bold yellow][dim] and run tests to track your progress![/dim]"
        )

    content = "\n".join(lines)
    panel = Panel(content, border_style="cyan", box=box.ROUNDED, expand=False)
    console.print(panel)


def draw_progress_bar(passed: int, total: int, width: int = 30) -> str:
    """Generate a colored Unicode text-based progress bar."""
    if total == 0:
        return ""
    percent = (passed / total) * 100
    filled = int(width * passed // total)
    bar = "█" * filled + "░" * (width - filled)

    if passed == total:
        color = "bold green"
    elif passed > 0:
        color = "bold yellow"
    else:
        color = "bold red"

    return f"[{color}][{bar}] {percent:5.1f}% ({passed}/{total})[/{color}]"


def display_dashboard(results: List[dict]):
    """Render a comprehensive Rich overview table of all tasks with progress."""
    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    pending = sum(1 for r in results if r["status"] == "NOT_IMPLEMENTED")
    failed = sum(1 for r in results if r["status"] == "FAILED")

    # Progress Summary Panel
    progress_bar = draw_progress_bar(passed, total, width=32)
    stats_text = (
        f"Progress: {progress_bar}\n"
        f"[green]✓ Passed: {passed}[/green]   "
        f"[yellow]○ Pending: {pending}[/yellow]   "
        f"[red]✗ Failed: {failed}[/red]   "
        f"[white]Total: {total}[/white]"
    )
    console.print(Panel(stats_text, title="[bold cyan]Challenge Progress[/bold cyan]", border_style="cyan", box=box.ROUNDED))

    # Tasks Table
    table = Table(
        title="[bold]Tasks & Test Status[/bold]",
        box=box.ROUNDED,
        header_style="bold magenta",
        expand=True,
    )
    table.add_column("#", style="bold cyan", width=5, justify="center")
    table.add_column("Category", style="blue", width=18)
    table.add_column("Target", style="green", width=22)
    table.add_column("Title", style="white")
    table.add_column("Status", justify="center", width=14)
    table.add_column("Time", justify="right", style="dim", width=8)

    for task in results:
        status = task["status"]
        if status == "PASSED":
            status_cell = "[bold green]✓ PASSED[/bold green]"
        elif status == "NOT_IMPLEMENTED":
            status_cell = "[dim yellow]○ PENDING[/dim yellow]"
        else:
            status_cell = "[bold red]✗ FAILED[/bold red]"

        duration = f"{task['duration_ms']:.1f}ms"
        table.add_row(
            f"#{task['id']:02d}",
            task["category"],
            f"{task['name']}()",
            task["title"],
            status_cell,
            duration,
        )

    console.print(table)

    if passed == total and total > 0:
        print_success_trophy()
    else:
        remaining = total - passed
        console.print(
            f"\n[yellow]💡 {remaining} task(s) remaining.[/yellow] "
            f"Open [bold yellow]{TARGET_FILE}[/bold yellow] to implement next functions, "
            f"or select options [bold][3][/bold]-[bold][5][/bold] for details, hints, and solutions.\n"
        )


def print_success_trophy():
    """Display celebration certificate when all exercises pass."""
    msg = Text()
    msg.append("🏆 CONGRATULATIONS! ALL TESTS PASSED! 🏆\n\n", style="bold green")
    msg.append("You have completed all tasks in this challenge.\n", style="bold white")
    if os.path.exists("app.py"):
        msg.append("Your application is fully functional! Test it with: poetry run app\n", style="italic green")
    msg.append("Great job mastering these Python concepts!\n", style="italic cyan")
    msg.append("Check solutions.md to compare your code with reference solutions.", style="dim")
    console.print(Panel(msg, border_style="green", box=box.DOUBLE, expand=False))


def find_target_symbol(task: dict):
    """Find the target function or class across app package/submodules or exercises."""
    name = task.get("name")
    if not name:
        return None, None, TARGET_FILE

    candidate_modules = []

    # 1. Check if task specifies an explicit module (e.g. "app.operations" or "operations")
    if "module" in task:
        try:
            mod = __import__(task["module"], fromlist=[task["module"].split(".")[-1]])
            candidate_modules.append(mod)
        except Exception:
            pass

    # 2. Check app package and submodules inside app/
    app_dir = os.path.join(ROOT_DIR, "app")
    if os.path.isdir(app_dir):
        try:
            import app
            candidate_modules.append(app)
        except Exception:
            pass

        try:
            for fname in sorted(os.listdir(app_dir)):
                if fname.endswith(".py") and not fname.startswith("__"):
                    sub_name = fname[:-3]
                    try:
                        sub_mod = __import__(f"app.{sub_name}", fromlist=[sub_name])
                        candidate_modules.append(sub_mod)
                    except Exception:
                        try:
                            sub_mod = __import__(sub_name)
                            candidate_modules.append(sub_mod)
                        except Exception:
                            pass
        except OSError:
            pass

    # 3. Check exercises or root app
    for mod_name in ("exercises", "app"):
        try:
            mod = __import__(mod_name)
            if mod not in candidate_modules:
                candidate_modules.append(mod)
        except ImportError:
            pass

    for mod in candidate_modules:
        if hasattr(mod, name):
            target = getattr(mod, name)
            try:
                src_file = inspect.getsourcefile(target) or getattr(mod, "__file__", "")
                if src_file:
                    rel_file = os.path.relpath(src_file, ROOT_DIR).replace("\\", "/")
                else:
                    rel_file = f"{mod.__name__}.py"
            except Exception:
                rel_file = f"{mod.__name__}.py"
            return target, mod, rel_file

    return None, None, TARGET_FILE


def show_task_detail(task_id: int):
    """Show comprehensive details for a specific task including docstring, source, and parsed test error."""
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if not task:
        console.print(f"[bold red]Invalid task ID: {task_id}[/bold red]")
        return

    fn, target_mod, file_label = find_target_symbol(task)
    doc = inspect.getdoc(fn) if fn else "No docstring available."
    source_code = inspect.getsource(fn) if fn else f"# Source code unavailable for {task['name']}."

    res = run_single_test(task["test"])

    # Header Panel
    console.print(
        Panel(
            f"[bold cyan]Task #{task['id']:02d}: {task['title']}[/bold cyan]\n"
            f"[white]Target:[/white] [bold green]{task['name']}()[/bold green] | "
            f"[white]Category:[/white] [bold blue]{task['category']}[/bold blue] | "
            f"[white]Test:[/white] [dim]{task['test']}[/dim]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )

    # Instructions / Docstring
    console.print(Panel(doc, title="[bold yellow]Instructions & Specification[/bold yellow]", border_style="yellow", box=box.ROUNDED))

    # Current Source Code
    syntax = Syntax(source_code, "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=f"[bold green]Current Implementation in {file_label}[/bold green]", border_style="green", box=box.ROUNDED))

    # Parsed Test Outcome
    status = res["status"]
    if status == "PASSED":
        result_text = f"[bold green]✓ PASSED[/bold green] [dim]({res['duration_ms']:.2f} ms)[/dim]\nAll unit tests passed successfully!"
        style = "green"
    elif status == "NOT_IMPLEMENTED":
        result_text = (
            f"[bold yellow]○ NOT IMPLEMENTED[/bold yellow]\n"
            f"The function raised [bold]NotImplementedError[/bold].\n"
            f"Open [bold yellow]{file_label}[/bold yellow] and replace the TODO with your solution."
        )
        style = "yellow"
    else:
        result_text = (
            f"[bold red]✗ FAILED[/bold red] [dim]({res['duration_ms']:.2f} ms)[/dim]\n"
            f"[bold white]Error Type:[/bold white] [bold red]{res['error_name']}[/bold red]\n"
            f"[bold white]Location:[/bold white] [cyan]{res['location']}[/cyan]\n"
            f"[bold white]Reason:[/bold white] [yellow]{res['message']}[/yellow]\n\n"
            f"[bold white]Traceback:[/bold white]\n[dim]{res['traceback'].strip()}[/dim]"
        )
        style = "red"

    console.print(Panel(result_text, title="[bold]Test Execution & Error Diagnostics[/bold]", border_style=style, box=box.ROUNDED))


def show_task_hints(task_id: int):
    """Display progressive hints for a specific task."""
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if not task:
        console.print(f"[bold red]Invalid task ID: {task_id}[/bold red]")
        return

    hints = task.get("hints", [])
    if not hints:
        console.print(f"[yellow]No hints available for Task #{task_id}.[/yellow]")
        return

    console.print(
        Panel(
            f"[bold cyan]Task #{task['id']:02d}: {task['title']}[/bold cyan]\n"
            f"[white]Target:[/white] [bold green]{task['name']}()[/bold green] | "
            f"[white]Category:[/white] [bold blue]{task['category']}[/bold blue]",
            title="[bold yellow]💡 Solution Hints[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
        )
    )

    for i, hint in enumerate(hints, 1):
        hint_panel = Panel(
            hint,
            title=f"[bold yellow]Hint {i} of {len(hints)}[/bold yellow]",
            border_style="dim yellow",
            box=box.ROUNDED,
        )
        console.print(hint_panel)


def show_task_solution(task_id: int):
    """Display reference solution for a specific task parsed from solutions.md."""
    task = next((t for t in TASKS if t["id"] == task_id), None)
    if not task:
        console.print(f"[bold red]Invalid task ID: {task_id}[/bold red]")
        return

    parsed = extract_task_solution(task_id)
    if not parsed or not parsed.get("code"):
        console.print(f"[red]Could not locate reference solution for Task #{task_id} in solutions.md.[/red]")
        return

    console.print(
        Panel(
            f"[bold cyan]Task #{task['id']:02d}: {task['title']}[/bold cyan]\n"
            f"[white]Target:[/white] [bold green]{task['name']}()[/bold green] | "
            f"[white]Source:[/white] [bold yellow]solutions.md[/bold yellow]",
            title="[bold green]📖 Reference Solution[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        )
    )

    # Reference Code
    syntax = Syntax(parsed["code"], "python", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="[bold green]Reference Code Implementation[/bold green]", border_style="green", box=box.ROUNDED))

    # Explanation Markdown
    if parsed.get("explanation"):
        md = Markdown(parsed["explanation"])
        console.print(Panel(md, title="[bold cyan]Explanation & Concepts[/bold cyan]", border_style="cyan", box=box.ROUNDED))


def show_solutions_hint():
    """Display general information regarding reference solutions."""
    if os.path.exists("solutions.md"):
        console.print(
            Panel(
                "Reference solutions are available in [bold green]solutions.md[/bold green]!\n"
                "You can also view task-specific solutions in this dashboard via menu option [bold][5][/bold]\n"
                "or CLI command: [bold yellow]python tui.py --solution <task_id>[/bold yellow].",
                title="[bold cyan]Reference Solutions Overview[/bold cyan]",
                border_style="cyan",
                box=box.ROUNDED,
            )
        )
    else:
        console.print("[dim]No solutions.md found in this repository.[/dim]")


# ==============================================================================
# MENU & CLI INTERFACE
# ==============================================================================
def interactive_menu():
    """Launch interactive CLI menu with Rich prompts."""
    print_banner(include_intro=True)
    while True:
        results = evaluate_all_tasks()
        passed = sum(1 for r in results if r["status"] == "PASSED")
        total = len(results)

        console.print(f"\n[bold cyan]─── CHALLENGE MENU ({passed}/{total} Completed) ───[/bold cyan]")
        console.print(" [bold][1][/bold] Show Dashboard / Task Overview")
        console.print(" [bold][2][/bold] Run Detailed Test Suite (Parsed Diagnostics)")
        console.print(" [bold][3][/bold] Inspect Task & Current Source Code")
        console.print(" [bold][4][/bold] View Extended Hints for a Task")
        console.print(" [bold][5][/bold] View Reference Solution for a Task (from solutions.md)")
        console.print(" [bold][6][/bold] Run Next Pending Task")
        has_app = HAS_APP_DIR or os.path.exists("app.py")
        if has_app:
            console.print(" [bold][7][/bold] Run Learning Application (poetry run app)")
        console.print(" [bold][0][/bold] Exit")

        choices = ["0", "1", "2", "3", "4", "5", "6"]
        if has_app:
            choices.append("7")

        try:
            choice = Prompt.ask("\n[bold]Select an option[/bold]", choices=choices, default="1")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if choice == "1":
            display_dashboard(results)
        elif choice == "2":
            run_tests_cli()
        elif choice == "3":
            task_input = Prompt.ask("Enter Task Number (ID)")
            if task_input.isdigit():
                show_task_detail(int(task_input))
            else:
                console.print("[red]Please enter a valid numeric ID.[/red]")
        elif choice == "4":
            task_input = Prompt.ask("Enter Task Number (ID) to view hints")
            if task_input.isdigit():
                show_task_hints(int(task_input))
            else:
                console.print("[red]Please enter a valid numeric ID.[/red]")
        elif choice == "5":
            task_input = Prompt.ask("Enter Task Number (ID) to view reference solution")
            if task_input.isdigit():
                show_task_solution(int(task_input))
            else:
                console.print("[red]Please enter a valid numeric ID.[/red]")
        elif choice == "6":
            next_task = next((t for t in results if t["status"] != "PASSED"), None)
            if next_task:
                show_task_detail(next_task["id"])
            else:
                print_success_trophy()
        elif choice == "7":
            console.print("\n[bold cyan]Launching learning application...[/bold cyan]\n")
            try:
                launched = False
                try:
                    from app.main import main as app_main
                    app_main()
                    launched = True
                except (ImportError, AttributeError):
                    pass

                if not launched:
                    try:
                        import app
                        if hasattr(app, "main"):
                            app.main()
                            launched = True
                    except Exception:
                        pass

                if not launched:
                    console.print("[yellow]Could not find main() in app/main.py or app.py.[/yellow]")
            except Exception as e:
                console.print(f"[bold red]Error running application:[/bold red] {e}")
        elif choice == "0":
            console.print("\n[green]Session ended. Happy coding![/green]")
            break


def run_tests_cli() -> int:
    """Run all tests with parsed output for CLI and Poetry script runner."""
    console.print("\n[bold cyan]Running Full Test Suite with Diagnostic Parsing...[/bold cyan]\n")
    results = evaluate_all_tasks()
    display_dashboard(results)

    passed = sum(1 for r in results if r["status"] == "PASSED")
    total = len(results)
    return 0 if (total > 0 and passed == total) else 1


def main():
    """Main CLI entry point supporting flags and interactive mode."""
    if "--task" in sys.argv:
        try:
            idx = sys.argv.index("--task")
            task_id = int(sys.argv[idx + 1])
            show_task_detail(task_id)
            sys.exit(0)
        except (IndexError, ValueError):
            console.print("[red]Usage: python tui.py --task <id>[/red]")
            sys.exit(1)

    if "--hint" in sys.argv:
        try:
            idx = sys.argv.index("--hint")
            task_id = int(sys.argv[idx + 1])
            show_task_hints(task_id)
            sys.exit(0)
        except (IndexError, ValueError):
            console.print("[red]Usage: python tui.py --hint <id>[/red]")
            sys.exit(1)

    if "--solution" in sys.argv:
        try:
            idx = sys.argv.index("--solution")
            task_id = int(sys.argv[idx + 1])
            show_task_solution(task_id)
            sys.exit(0)
        except (IndexError, ValueError):
            console.print("[red]Usage: python tui.py --solution <id>[/red]")
            sys.exit(1)

    if "--solutions" in sys.argv:
        show_solutions_hint()
        sys.exit(0)

    if "--check" in sys.argv or "--status" in sys.argv:
        print_banner(include_intro=True)
        results = evaluate_all_tasks()
        display_dashboard(results)
        passed = sum(1 for r in results if r["status"] == "PASSED")
        sys.exit(0 if len(results) > 0 and passed == len(results) else 1)
    elif "--test" in sys.argv:
        exit_code = run_tests_cli()
        sys.exit(exit_code)
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
