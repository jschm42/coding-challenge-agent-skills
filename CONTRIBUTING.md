# Contributing to the Skills Collection

Thank you for your interest in contributing to this skills repository! We welcome new skills, improvements to existing skills, and bug fixes.

---

## 📋 Skill Authoring Guidelines

Every skill in this repository must adhere to the Antigravity Skill Specification:

1. **Location**: Place each skill in `skills/<skill-name>/`.
2. **Naming**: Use lowercase, hyphenated names (e.g. `fastapi-scaffolder`). The directory name must match the `name:` field in `SKILL.md`.
3. **`SKILL.md` File**:
   - Must begin with a valid YAML frontmatter block containing `name` and `description`.
   - The `description` must clearly articulate in third person **what** the skill does and **when** the agent should activate it.
4. **Self-Contained**: Any templates, scripts, or assets needed by the skill must be placed inside that skill's directory (e.g. `skills/<skill-name>/templates/`).
5. **English**: All skill instructions, docstrings, and templates must be written in English.

---

## 🧪 Validating Your Skill

Before submitting a Pull Request, run the validation test suite locally:

```bash
python tests/test_skills_syntax.py
```

The test runner will automatically check:
- Valid YAML frontmatter format
- Matching skill directory and name
- Non-empty, comprehensive description
- Integrity of all relative markdown links

---

## 🚀 Submitting a Pull Request

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-new-skill`.
3. Commit your changes: `git commit -m "feat(skill): add my-new-skill"`.
4. Push to your branch and open a Pull Request.
