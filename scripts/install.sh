#!/usr/bin/env bash
# ==============================================================================
# Antigravity Skills Installer for Linux & macOS
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SOURCE_SKILLS_DIR="$REPO_ROOT/skills"

if [ ! -d "$SOURCE_SKILLS_DIR" ]; then
    echo "[ERROR] Source skills directory not found at $SOURCE_SKILLS_DIR"
    exit 1
fi

DEST_DIR=""
GLOBAL_INSTALL=false
SPECIFIC_SKILL=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --global|-g) GLOBAL_INSTALL=true ;;
        --target|-t) DEST_DIR="$2/.agents/skills"; shift ;;
        --skill|-s) SPECIFIC_SKILL="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

if [ "$GLOBAL_INSTALL" = true ]; then
    DEST_DIR="$HOME/.gemini/config/skills"
elif [ -z "$DEST_DIR" ]; then
    echo "=========================================================="
    echo " Antigravity Skills Installer (Bash)"
    echo "=========================================================="
    echo "Please choose installation destination:"
    echo " [1] Global: Install to ~/.gemini/config/skills/ (available everywhere)"
    echo " [2] Local Project: Enter path to an existing project"
    echo " [0] Cancel"
    read -p "Select option [1/2/0]: " choice
    case $choice in
        1) DEST_DIR="$HOME/.gemini/config/skills" ;;
        2) 
            read -p "Enter project root directory: " project_path
            if [ ! -d "$project_path" ]; then
                echo "[ERROR] Directory does not exist: $project_path"
                exit 1
            fi
            DEST_DIR="$project_path/.agents/skills"
            ;;
        *) echo "Installation cancelled."; exit 0 ;;
    esac
fi

mkdir -p "$DEST_DIR"
echo ""
echo "[INFO] Installing skills to: $DEST_DIR"

if [ -n "$SPECIFIC_SKILL" ]; then
    SKILL_PATH="$SOURCE_SKILLS_DIR/$SPECIFIC_SKILL"
    if [ ! -d "$SKILL_PATH" ]; then
        echo "[ERROR] Skill '$SPECIFIC_SKILL' not found in $SOURCE_SKILLS_DIR"
        exit 1
    fi
    cp -r "$SKILL_PATH" "$DEST_DIR/"
    echo "  ✓ Installed skill: $SPECIFIC_SKILL"
else
    for skill_path in "$SOURCE_SKILLS_DIR"/*; do
        if [ -d "$skill_path" ]; then
            skill_name=$(basename "$skill_path")
            cp -r "$skill_path" "$DEST_DIR/"
            echo "  ✓ Installed skill: $skill_name"
        fi
    done
fi

echo ""
echo "[SUCCESS] All skills installed successfully!"
echo "Restart or open Antigravity / Agent session to use the new skills."
