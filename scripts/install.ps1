<#
.SYNOPSIS
    Antigravity Skills Installer for Windows (PowerShell)

.DESCRIPTION
    Installs skills from this repository either globally (~/.gemini/config/skills/)
    or into a specific project's workspace (.agents/skills/).

.PARAMETER Global
    Installs skills into the user's global Antigravity config directory.

.PARAMETER TargetPath
    Path to a target project where skills should be copied to .agents/skills/.

.PARAMETER Skill
    Specific skill name to install (default: all skills).

.EXAMPLE
    .\scripts\install.ps1 -Global
    .\scripts\install.ps1 -TargetPath "C:\Projects\my-project"
    .\scripts\install.ps1 -Global -Skill "generate-python-exercise-project"
#>

[CmdletBinding()]
param(
    [switch]$Global,
    [string]$TargetPath,
    [string]$Skill = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$SourceSkillsDir = Join-Path $RepoRoot "skills"

if (-not (Test-Path $SourceSkillsDir)) {
    Write-Error "Source skills directory not found at: $SourceSkillsDir"
}

# Determine destination
if ($Global) {
    $UserHome = [System.Environment]::GetFolderPath('UserProfile')
    $DestDir = Join-Path $UserHome ".gemini\config\skills"
} elseif ($TargetPath) {
    if (-not (Test-Path $TargetPath)) {
        Write-Error "Target path does not exist: $TargetPath"
    }
    $DestDir = Join-Path $TargetPath ".agents\skills"
} else {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host " Antigravity Skills Installer (Windows)" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "Please choose installation destination:"
    Write-Host " [1] Global: Install to ~/.gemini/config/skills/ (available in all workspaces)"
    Write-Host " [2] Local Project: Enter path to an existing project"
    Write-Host " [0] Cancel"
    
    $choice = Read-Host "Select option [1/2/0]"
    if ($choice -eq "1") {
        $UserHome = [System.Environment]::GetFolderPath('UserProfile')
        $DestDir = Join-Path $UserHome ".gemini\config\skills"
    } elseif ($choice -eq "2") {
        $inputPath = Read-Host "Enter project root directory"
        if (-not (Test-Path $inputPath)) {
            Write-Error "Provided path does not exist: $inputPath"
        }
        $DestDir = Join-Path $inputPath ".agents\skills"
    } else {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Ensure destination directory exists
if (-not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
    Write-Host "[INFO] Created directory: $DestDir" -ForegroundColor Gray
}

# Get list of skills to copy
if ($Skill) {
    $SkillDirs = Get-ChildItem -Path $SourceSkillsDir -Directory | Where-Object { $_.Name -eq $Skill }
    if ($SkillDirs.Count -eq 0) {
        Write-Error "Skill '$Skill' not found in $SourceSkillsDir"
    }
} else {
    $SkillDirs = Get-ChildItem -Path $SourceSkillsDir -Directory
}

Write-Host "`n[INFO] Installing skills to: $DestDir" -ForegroundColor Cyan
foreach ($sDir in $SkillDirs) {
    $destSkillPath = Join-Path $DestDir $sDir.Name
    Copy-Item -Path $sDir.FullName -Destination $destSkillPath -Recurse -Force
    Write-Host "  ✓ Installed skill: $($sDir.Name)" -ForegroundColor Green
}

Write-Host "`n[SUCCESS] All skills installed successfully!" -ForegroundColor Green
Write-Host "Restart or open Antigravity / Agent session to use the new skills.`n" -ForegroundColor Gray
