#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  Setting up Python Challenge Environment"
echo "========================================================"

if command -v poetry &> /dev/null; then
    echo "[INFO] Found Poetry. Installing dependencies..."
    if poetry install; then
        echo ""
        echo "========================================================"
        echo "  Setup completed successfully with Poetry!"
        echo "  - Run app:   poetry run app"
        echo "  - Run tests: poetry run test"
        echo "========================================================"
        exit 0
    else
        echo "[WARNING] poetry install encountered an issue. Falling back to pip..."
    fi
else
    echo "[INFO] Poetry not found in PATH. Checking python3 and pip..."
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "[ERROR] Python was not found in PATH. Please install Python 3.10+."
        exit 1
    fi
fi

echo "Installing dependencies via pip..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install "rich>=13.7.0"

echo ""
echo "========================================================"
echo "  Setup completed successfully with pip!"
echo "  - Run app:   $PYTHON_CMD app.py"
echo "  - Run tests: $PYTHON_CMD app.py --test"
echo "========================================================"
