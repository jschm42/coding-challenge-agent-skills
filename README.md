# ⚡ Antigravity Skills Collection

A curated collection of modular, production-ready **Skills** for [Google Antigravity](https://antigravity.google) and compatible AI coding agents.

Extend your agent with specialized workflows, code generators, interactive training builders, and architectural scaffolds.

---

## 📚 Skills Catalog

| Skill Name | Slash Command | Category | Description |
| :--- | :--- | :--- | :--- |
| [**generate-python-exercise-project**](./skills/generate-python-exercise-project/) | `/generate-python-exercise-project` | `Python`, `Education` | Generates interactive coding challenges with Rich TUI, test parsing, hints, and reference solutions |

*(More skills coming soon! Contributions welcome!)*

---

## 🚀 Quickstart Installation

You can install skills either **globally** (available in all projects on your machine) or **locally** (scoped to a specific project).

### Method 1: Using the Automated Installer

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

---

### Method 2: Manual Copying

Simply copy any skill folder from `skills/<skill-name>` into:
* **Global:** `~/.gemini/config/skills/<skill-name>/`
* **Local Project:** `<project-root>/.agents/skills/<skill-name>/`

---

## 🎯 How to Use Skills in Antigravity

Once installed, skills are automatically discovered by Antigravity using **progressive disclosure**:

1. **Via Slash Command:**
   ```text
   /generate-python-exercise-project Create an interactive challenge for Python sets with 8 exercises
   ```

2. **Via Natural Language Prompt:**
   > *"Generate an interactive Python challenge on list comprehension with 5 exercises."*

The agent reads the skill's `SKILL.md` instructions and executes the workflow autonomously.

---

## 🧪 Testing & Validation

All skills in this repository are validated automatically via CI and can be verified locally:

```bash
python tests/test_skills_syntax.py
```

This ensures:
- Valid YAML frontmatter syntax
- Matching skill directory names
- Complete descriptions for agent discovery
- Integrity of all relative links and templates

---

## 🤝 Contributing

Contributions of new skills or improvements are warmly welcomed! Please read our [CONTRIBUTING.md](./CONTRIBUTING.md) guide before opening a Pull Request.

---

## 📄 License

This repository is licensed under the [MIT License](./LICENSE).
