#!/usr/bin/env python3
"""
Executable Learning Application Template (app/main.py)
======================================================
Interactive application entry point (e.g., Calculator, CLI tool, or interactive app).
For Clean Code structure, domain functions can also be extracted into modular files
under app/ (e.g., app/operations.py) and imported here.

Usage:
    poetry run app
or:
    python app/main.py
"""

import sys
from typing import Any, List, Optional, Tuple


def add(a: float, b: float) -> float:
    """Add two numbers and return the sum.

    Examples:
        >>> add(2.0, 3.0)
        5.0
        >>> add(-1.5, 2.5)
        1.0
    """
    # TODO: Task 1 - Implement addition
    raise NotImplementedError("Task 1: add() not implemented yet!")


def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the difference.

    Examples:
        >>> subtract(10.0, 4.0)
        6.0
    """
    # TODO: Task 2 - Implement subtraction
    raise NotImplementedError("Task 2: subtract() not implemented yet!")


def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product.

    Examples:
        >>> multiply(3.0, 4.0)
        12.0
    """
    # TODO: Task 3 - Implement multiplication
    raise NotImplementedError("Task 3: multiply() not implemented yet!")


def divide(a: float, b: float) -> float:
    """Divide a by b and return the quotient.

    Raises:
        ValueError: If b is 0.

    Examples:
        >>> divide(10.0, 2.0)
        5.0
    """
    # TODO: Task 4 - Implement division with zero check
    raise NotImplementedError("Task 4: divide() not implemented yet!")


def parse_expression(expression: str) -> Tuple[float, str, float]:
    """Parse a simple arithmetic expression string into (operand1, operator, operand2).

    Supported operators: '+', '-', '*', '/'

    Raises:
        ValueError: If the expression format is invalid or operator is unsupported.

    Examples:
        >>> parse_expression("12 + 5")
        (12.0, '+', 5.0)
    """
    # TODO: Task 5 - Parse expression string into operands and operator
    raise NotImplementedError("Task 5: parse_expression() not implemented yet!")


def calculate(expression: str) -> float:
    """Evaluate a mathematical expression string using the helper functions above.

    Examples:
        >>> calculate("8 * 7")
        56.0
    """
    # TODO: Task 6 - Combine parsing and operation execution
    raise NotImplementedError("Task 6: calculate() not implemented yet!")


def run_cli_loop():
    """Run interactive REPL loop for the executable application."""
    print("=" * 55)
    print("  Interactive Application (Learner App)")
    print("  Type an expression (e.g., '12 + 5') or 'quit' to exit.")
    print("  To track progress or view hints, run: poetry run tui")
    print("=" * 55)

    while True:
        try:
            user_input = input("app> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Goodbye!")
                break
            if user_input.lower() == "help":
                print("Available commands:")
                print("  <expr>   - Evaluate math expression (e.g. 5 * 3)")
                print("  help     - Show this help message")
                print("  quit     - Exit the application")
                continue

            result = calculate(user_input)
            print(f"= {result}")
        except NotImplementedError as e:
            print(f"[PENDING] {e}")
            print("Tip: Implement the function in app.py or run 'poetry run tui' for hints.")
        except ValueError as e:
            print(f"[ERROR] Invalid input: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nSession interrupted. Exiting.")
            break


def main():
    """Main application entry point."""
    if len(sys.argv) > 1:
        expr = " ".join(sys.argv[1:])
        try:
            print(calculate(expr))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        run_cli_loop()


if __name__ == "__main__":
    main()
