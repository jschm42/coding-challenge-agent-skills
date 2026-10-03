# 🎯 Coding Challenge Agent Skills

A modular collection of AI Agent **Skills** designed to autonomously scaffold and generate **interactive coding exercises and challenge projects**.

While originally designed with [Google Antigravity](https://antigravity.google) conventions, these skills follow an **open, file-based specification** (`SKILL.md` with YAML frontmatter) and are fully portable across **any modern AI coding agent** (Claude Code, Cursor, Windsurf, Aider, OpenCode, etc.).

---

## 💡 What are Coding Challenge Skills?

Rather than writing exercises by hand, these skills teach your AI agent how to build **complete, didactic, and fun coding practice environments** from a single prompt.

* **🎯 Primary Focus:** Generating complete coding exercise repositories with automated test runners, hint tiers, and progressive difficulty.
* **🐍 Current Scope:** **Python first** — producing terminal-based exercises featuring interactive [Rich](https://github.com/Textualize/rich) TUIs, unit test evaluation, hint systems, and verified solutions.
* **🔮 Roadmap:** Future challenge scaffolds for TypeScript/JavaScript, Go, Rust, and SQL.
* **🤖 Universal Agent Support:** Usable across Google Antigravity, Claude Code, Cursor, Windsurf, and custom LLM workflows.

---

## 📚 Skills Catalog

| Skill Name | Scope | Compatible Agents | Description |
| :--- | :--- | :--- | :--- |
| [**generate-python-exercise-project**](./skills/generate-python-exercise-project/) | `Python` | Antigravity, Claude Code, Cursor, Windsurf, Aider | Scaffolds interactive Python coding challenges with Rich TUI, automated test parsing, multi-tier hints, and clean solutions. |

*(More language generators coming soon! Contributions welcome!)*

---

## 🤖 Cross-Agent Compatibility

These skills are completely self-contained markdown workflows with bundled templates. You can use them with:

* **Google Antigravity:** Native auto-discovery via `~/.gemini/config/skills/` (global) or `.agents/skills/` (project-level).
* **Claude Code:** Place into your project or reference directly via custom commands / system prompts.
* **Cursor & Windsurf:** Reference via `.cursorrules`, `.windsurfrules`, or place in your workspace instructions.
* **Aider & Other LLM CLIs:** Pass `skills/<skill-name>/SKILL.md` as context or system instructions.

---

## 🚀 Quickstart Installation

You can install skills globally (for all projects on your machine) or locally (scoped to a specific project).

### Method 1: Instant via `npx` (No clone needed)

Run the interactive installer directly in your terminal without cloning the repository:

```bash
# Run interactively via GitHub:
npx github:jschm42/coding-challenge-agent-skills

# Or non-interactively with flags:
npx github:jschm42/coding-challenge-agent-skills --target ./my-project --skill generate-python-exercise-project
npx github:jschm42/coding-challenge-agent-skills --global --all
```

*(Once published to npm, you can simply run `npx coding-challenge-agent-skills`)*

Alternatively, download a specific skill folder using `npx degit`:
```bash
npx degit jschm42/coding-challenge-agent-skills/skills/generate-python-exercise-project .agents/skills/generate-python-exercise-project
```

### Method 2: Automated Install Scripts

#### 🪟 Windows (PowerShell)
```powershell
# Interactive menu:
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1

# Or install all skills globally (~/.gemini/config/skills/):
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Global

# Or install into a specific project (.agents/skills/):
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -TargetPath "C:\Path\To\YourProject"
```

#### 🐧 Linux & macOS (Bash)
```bash
# Interactive menu:
chmod +x ./scripts/install.sh && ./scripts/install.sh

# Or install all skills globally:
./scripts/install.sh --global

# Or install into a specific project:
./scripts/install.sh --target /path/to/your/project
```

### Method 3: Manual Copying

Simply copy the desired folder from `skills/<skill-name>` into:
* **Antigravity Global:** `~/.gemini/config/skills/<skill-name>/`
* **Local Project (Standard):** `<project-root>/.agents/skills/<skill-name>/`

---

## 🎯 How to Use (Example: Python Challenge Generator)

Once available in your agent's context, trigger it naturally or via slash command:

1. **Via Slash Command (Antigravity):**
   ```text
   /generate-python-exercise-project Create an interactive challenge for Python decorators with 6 exercises
   ```

2. **Via Natural Language (Any Agent):**
   > *"Generate an interactive Python challenge on list comprehensions with 5 exercises based on the generate-python-exercise-project skill."*

The agent reads [SKILL.md](./skills/generate-python-exercise-project/SKILL.md), plans the exercise set, and instantiates the template files.

---

## 🧪 Testing & Validation

Skills syntax and relative template references are validated automatically:

```bash
python tests/test_skills_syntax.py
```

---

## 🤝 Contributing

We welcome additions of new challenge generator skills (Python variations or new languages)! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

---

## 📄 License

This repository is licensed under the [MIT License](./LICENSE).
