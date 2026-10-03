#!/usr/bin/env python3
"""
Automated Skill Validation Test Suite
====================================
Validates all skills in the skills/ directory against the Antigravity skill specification:
- Ensures SKILL.md exists in every skill folder
- Verifies YAML frontmatter structure (name, description)
- Verifies directory name matches skill name
- Checks for broken relative file links in SKILL.md
"""

import os
import re
import sys
import unittest
from pathlib import Path


class TestSkillsRepository(unittest.TestCase):
    """Test suite validating all skills in this repository."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.skills_dir = cls.repo_root / "skills"

    def test_skills_directory_exists(self):
        """Verify the skills/ root directory exists and contains at least one skill."""
        self.assertTrue(self.skills_dir.exists(), "skills/ directory must exist")
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir()]
        self.assertGreater(len(skill_dirs), 0, "skills/ must contain at least one skill folder")

    def test_all_skills_conform_to_schema(self):
        """Iterate through every skill and validate SKILL.md and structure."""
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir()]

        for sdir in skill_dirs:
            skill_name = sdir.name
            with self.subTest(skill=skill_name):
                skill_file = sdir / "SKILL.md"
                self.assertTrue(skill_file.exists(), f"Missing SKILL.md in {sdir}")

                content = skill_file.read_text(encoding="utf-8")

                # Validate frontmatter presence
                fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
                self.assertIsNotNone(
                    fm_match,
                    f"SKILL.md in {skill_name} must begin with YAML frontmatter delimited by '---'",
                )

                frontmatter_text = fm_match.group(1)

                # Validate 'name' field
                name_match = re.search(r"^name:\s*([a-zA-Z0-9_\-]+)\s*$", frontmatter_text, re.MULTILINE)
                self.assertIsNotNone(name_match, f"'name' field missing or invalid in {skill_name}")
                declared_name = name_match.group(1)
                self.assertEqual(
                    declared_name,
                    skill_name,
                    f"Declared skill name '{declared_name}' must match directory name '{skill_name}'",
                )

                # Validate 'description' field
                desc_match = re.search(r"^description:\s*(?:>-|>|\|)?\s*\n?(.*?)(?=\n[a-zA-Z0-9_\-]+:|\Z)", frontmatter_text, re.DOTALL | re.MULTILINE)
                self.assertIsNotNone(desc_match, f"'description' field missing in {skill_name}")
                desc_content = desc_match.group(1).strip()
                self.assertGreater(len(desc_content), 15, f"Description in {skill_name} is too short")

                # Validate local relative links in SKILL.md
                # Matches markdown links of form [label](./path) or [label](path)
                links = re.findall(r"\[.*?\]\((?!http|https|mailto|file:)(.*?)\)", content)
                for link in links:
                    clean_link = link.split("#")[0].strip()
                    if not clean_link:
                        continue
                    target_path = (sdir / clean_link).resolve()
                    self.assertTrue(
                        target_path.exists(),
                        f"Broken link in {skill_name}/SKILL.md: '{link}' -> resolved to non-existent '{target_path}'",
                    )


if __name__ == "__main__":
    unittest.main()
