#!/usr/bin/env python3
"""Generate assets/tui_dashboard.svg showcasing the Rich TUI Dashboard."""

import sys
import os

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.system("")

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console(record=True, width=100)

banner_text = (
    "[bold cyan]PYTHON APPLICATION CHALLENGE: CALCULATOR CLI[/bold cyan]\n"
    "[italic white]Master Python step by step with real-time test feedback & Rich TUI[/italic white]\n\n"
    "[dim]Solve tasks in [/dim][bold yellow]app.py[/bold yellow][dim] | "
    "Run app: [/dim][bold green]poetry run app[/bold green][dim] | "
    "Track progress: [/dim][bold cyan]poetry run tui[/bold cyan]"
)
console.print(Panel(banner_text, border_style="cyan", box=box.ROUNDED))

stats_text = (
    "Progress: [bold yellow][████████████████░░░░░░░░░░░░░░░░]  50.0% (3/6)[/bold yellow]\n"
    "[green]✓ Passed: 3[/green]   "
    "[yellow]○ Pending: 2[/yellow]   "
    "[red]✗ Failed: 1[/red]   "
    "[white]Total: 6[/white]"
)
console.print(Panel(stats_text, title="[bold cyan]Challenge Progress[/bold cyan]", border_style="cyan", box=box.ROUNDED))

table = Table(
    title="[bold]Tasks & Test Status[/bold]",
    box=box.ROUNDED,
    header_style="bold magenta",
    expand=True,
)
table.add_column("#", style="bold cyan", width=5, justify="center")
table.add_column("Category", style="blue", width=16)
table.add_column("Target", style="green", width=22)
table.add_column("Title", style="white")
table.add_column("Status", justify="center", width=14)
table.add_column("Time", justify="right", style="dim", width=8)

table.add_row("#01", "Basic Ops", "add()", "Implement basic addition", "[bold green]✓ PASSED[/bold green]", "1.2ms")
table.add_row("#02", "Basic Ops", "subtract()", "Implement basic subtraction", "[bold green]✓ PASSED[/bold green]", "0.9ms")
table.add_row("#03", "Basic Ops", "multiply()", "Implement multiplication", "[bold green]✓ PASSED[/bold green]", "1.1ms")
table.add_row("#04", "Basic Ops", "divide()", "Implement division & zero check", "[bold red]✗ FAILED[/bold red]", "2.4ms")
table.add_row("#05", "Parsing", "parse_expression()", "Parse expression string", "[dim yellow]○ PENDING[/dim yellow]", "0.0ms")
table.add_row("#06", "Application", "calculate()", "Full expression evaluation", "[dim yellow]○ PENDING[/dim yellow]", "0.0ms")

console.print(table)

menu_text = (
    "\n[bold cyan]─── CHALLENGE MENU (3/6 Completed) ───[/bold cyan]\n"
    " [bold][1][/bold] Show Dashboard / Task Overview\n"
    " [bold][2][/bold] Run Detailed Test Suite (Parsed Diagnostics)\n"
    " [bold][3][/bold] Inspect Task & Current Source Code\n"
    " [bold][4][/bold] View Extended Hints for a Task\n"
    " [bold][5][/bold] View Reference Solution for a Task (from solutions.md)\n"
    " [bold][6][/bold] Run Next Pending Task\n"
    " [bold][7][/bold] Run Learning Application (app.py)\n"
    " [bold][0][/bold] Exit\n\n"
    "[bold]Select an option [0-7] (default 1):[/bold] 1"
)
console.print(menu_text)

os.makedirs("assets", exist_ok=True)
console.save_svg("assets/tui_dashboard.svg", title="Python Challenge TUI Dashboard")
print("Saved assets/tui_dashboard.svg successfully!")
