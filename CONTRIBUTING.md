# Contributing to Coding Challenge Agent Skills

Thank you for your interest in contributing! This project provides modular skills that teach AI coding agents how to autonomously generate **interactive coding exercises and challenges**.

We welcome contributions of new challenge skills (expanding our Python generators or introducing new languages like TypeScript, Rust, Go), as well as improvements to existing templates and documentation.

---

## 🎯 What We're Looking For

* **New Language Challenge Scaffolds:** Generators that scaffold exercises for languages such as TypeScript (Jest/Vitest), Rust (Cargo tests), Go (`go test`), or SQL.
* **Specialized Challenge Frameworks:** Generators targeting specific paradigms (e.g. async Python, data structures & algorithms, web APIs).
* **Cross-Agent Enhancements:** Ensuring skills work seamlessly in Antigravity, Claude Code, Cursor, Windsurf, Aider, etc.

---

## 📋 Skill Authoring Guidelines

Every skill in this repository must follow the open skill standard:

1. **Location**: Place each skill in `skills/<skill-name>/`.
2. **Naming**: Use lowercase, hyphenated names (e.g. `generate-python-exercise-project`, `generate-typescript-exercise-project`). The directory name must match the `name:` field in `SKILL.md`.
3. **`SKILL.md` File**:
   - Must begin with a valid YAML frontmatter block containing `name` and `description`.
   - The `description` must clearly articulate in third person **what** the skill generates and **when** the agent should activate it.
   - Instructions should be generic enough so any LLM-powered coding agent can interpret and run them.
4. **Self-Contained**: Any templates, scripts, or assets needed by the skill must be placed inside that skill's directory (e.g. `skills/<skill-name>/templates/`).
5. **Language**: All skill instructions, docstrings, and templates must be written in English.

---

## 🧪 Validating Your Skill

Before submitting a Pull Request, run the validation test suite locally:

```bash
python tests/test_skills_syntax.py
```

The test runner automatically checks:
- Valid YAML frontmatter format
- Matching skill directory and skill name
- Non-empty, comprehensive description
- Integrity of all relative markdown links and template references

---

## 🚀 Submitting a Pull Request

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/generate-ts-exercise-project`.
3. Commit your changes: `git commit -m "feat(skill): add TypeScript exercise generator skill"`.
4. Push to your branch and open a Pull Request.

