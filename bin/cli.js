#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import readline from 'node:readline/promises';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const SKILLS_DIR = path.join(REPO_ROOT, 'skills');

// ANSI Colors
const colors = {
  reset: '\x1b[0m',
  cyan: '\x1b[36m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  bold: '\x1b[1m',
  gray: '\x1b[90m'
};

function printBanner() {
  console.log(`\n${colors.cyan}${colors.bold}🎯 Coding Challenge Agent Skills Installer${colors.reset}`);
  console.log(`${colors.gray}Modular skills for AI coding agents (Antigravity, Claude Code, Cursor, Windsurf)${colors.reset}\n`);
}

function printHelp() {
  printBanner();
  console.log(`Usage:
  ${colors.bold}npx coding-challenge-agent-skills${colors.reset} [options]
  ${colors.bold}node bin/cli.js${colors.reset} [options]

Options:
  -h, --help            Show this help message
  -l, --list            List all available skills
  -g, --global          Install globally for Google Antigravity (~/.gemini/config/skills/)
  -t, --target <path>   Target directory for installation (installs into <path>/.agents/skills/)
  -s, --skill <name>    Install a specific skill (default: prompt or all)
  -a, --all             Install all available skills without prompting

Examples:
  npx coding-challenge-agent-skills
  npx coding-challenge-agent-skills --target ./my-project
  npx coding-challenge-agent-skills --global --skill generate-python-exercise-project
`);
}

function getAvailableSkills() {
  if (!fs.existsSync(SKILLS_DIR)) {
    console.error(`${colors.red}Error: Skills directory not found at ${SKILLS_DIR}${colors.reset}`);
    process.exit(1);
  }
  return fs.readdirSync(SKILLS_DIR, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
}

function copySkill(skillName, destDir) {
  const source = path.join(SKILLS_DIR, skillName);
  const target = path.join(destDir, skillName);

  if (!fs.existsSync(source)) {
    console.error(`${colors.red}✗ Skill '${skillName}' not found in ${SKILLS_DIR}${colors.reset}`);
    return false;
  }

  fs.mkdirSync(destDir, { recursive: true });
  fs.cpSync(source, target, { recursive: true, force: true });
  console.log(`  ${colors.green}✓${colors.reset} Installed: ${colors.bold}${skillName}${colors.reset}`);
  return true;
}

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('-h') || args.includes('--help')) {
    printHelp();
    return;
  }

  const availableSkills = getAvailableSkills();

  if (args.includes('-l') || args.includes('--list')) {
    printBanner();
    console.log(`${colors.bold}Available Skills:${colors.reset}`);
    for (const skill of availableSkills) {
      console.log(`  • ${colors.cyan}${skill}${colors.reset}`);
    }
    console.log();
    return;
  }

  let isGlobal = args.includes('-g') || args.includes('--global');
  let targetArg = null;
  let targetIdx = args.findIndex(arg => arg === '-t' || arg === '--target');
  if (targetIdx !== -1 && args[targetIdx + 1]) {
    targetArg = args[targetIdx + 1];
  }

  let skillArg = null;
  let skillIdx = args.findIndex(arg => arg === '-s' || arg === '--skill');
  if (skillIdx !== -1 && args[skillIdx + 1]) {
    skillArg = args[skillIdx + 1];
  }

  let installAll = args.includes('-a') || args.includes('--all');

  let destDir = null;

  if (isGlobal) {
    destDir = path.join(os.homedir(), '.gemini', 'config', 'skills');
  } else if (targetArg) {
    const resolvedTarget = path.resolve(targetArg);
    if (!fs.existsSync(resolvedTarget)) {
      fs.mkdirSync(resolvedTarget, { recursive: true });
    }
    // If target already ends with .agents/skills or skills, use it, otherwise append .agents/skills
    if (resolvedTarget.endsWith('.agents' + path.sep + 'skills') || resolvedTarget.endsWith('skills')) {
      destDir = resolvedTarget;
    } else {
      destDir = path.join(resolvedTarget, '.agents', 'skills');
    }
  }

  let skillsToInstall = [];
  if (skillArg) {
    if (!availableSkills.includes(skillArg)) {
      console.error(`${colors.red}Error: Unknown skill '${skillArg}'. Available: ${availableSkills.join(', ')}${colors.reset}`);
      process.exit(1);
    }
    skillsToInstall = [skillArg];
  } else if (installAll) {
    skillsToInstall = availableSkills;
  }

  // Interactive flow if missing destination or skill choices
  if (!destDir || skillsToInstall.length === 0) {
    printBanner();
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    try {
      if (skillsToInstall.length === 0) {
        console.log(`${colors.bold}Which skill(s) would you like to install?${colors.reset}`);
        availableSkills.forEach((s, i) => {
          console.log(`  [${i + 1}] ${s}`);
        });
        console.log(`  [A] All skills (${availableSkills.length})`);
        console.log(`  [0] Cancel\n`);

        const answer = (await rl.question(`Select option [1-${availableSkills.length}/A/0]: `)).trim();
        if (answer === '0' || answer === '') {
          console.log(`${colors.yellow}Installation cancelled.${colors.reset}`);
          rl.close();
          return;
        }

        if (answer.toLowerCase() === 'a') {
          skillsToInstall = availableSkills;
        } else {
          const num = parseInt(answer, 10);
          if (isNaN(num) || num < 1 || num > availableSkills.length) {
            console.error(`${colors.red}Invalid option.${colors.reset}`);
            rl.close();
            process.exit(1);
          }
          skillsToInstall = [availableSkills[num - 1]];
        }
      }

      if (!destDir) {
        console.log(`\n${colors.bold}Where should the skill(s) be installed?${colors.reset}`);
        console.log(`  [1] Current directory: ./.agents/skills/ (Standard for AI agents)`);
        console.log(`  [2] Global Antigravity: ~/.gemini/config/skills/ (Available everywhere)`);
        console.log(`  [3] Custom project path`);
        console.log(`  [0] Cancel\n`);

        const locationChoice = (await rl.question(`Select destination [1/2/3/0]: `)).trim();
        if (locationChoice === '1') {
          destDir = path.resolve(process.cwd(), '.agents', 'skills');
        } else if (locationChoice === '2') {
          destDir = path.join(os.homedir(), '.gemini', 'config', 'skills');
        } else if (locationChoice === '3') {
          const customPath = (await rl.question(`Enter project root or target directory: `)).trim();
          if (!customPath) {
            console.log(`${colors.yellow}Installation cancelled.${colors.reset}`);
            rl.close();
            return;
          }
          const resolved = path.resolve(customPath);
          if (!fs.existsSync(resolved)) {
            console.error(`${colors.red}Target path does not exist: ${resolved}${colors.reset}`);
            rl.close();
            process.exit(1);
          }
          destDir = resolved.endsWith('.agents' + path.sep + 'skills') || resolved.endsWith('skills')
            ? resolved
            : path.join(resolved, '.agents', 'skills');
        } else {
          console.log(`${colors.yellow}Installation cancelled.${colors.reset}`);
          rl.close();
          return;
        }
      }
    } finally {
      rl.close();
    }
  }

  console.log(`\n${colors.cyan}Installing to:${colors.reset} ${destDir}\n`);
  for (const s of skillsToInstall) {
    copySkill(s, destDir);
  }

  console.log(`\n${colors.green}${colors.bold}✨ Successfully installed!${colors.reset}`);
  console.log(`${colors.gray}The installed skills are ready to be used by your AI coding agent.${colors.reset}\n`);
}

main().catch(err => {
  console.error(`${colors.red}Unexpected error:${colors.reset}`, err);
  process.exit(1);
});
