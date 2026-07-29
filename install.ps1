$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

python -m pip install -r (Join-Path $RepoRoot "requirements.txt")

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "Codex CLI is required. Install it, then rerun this script."
}

codex plugin marketplace add $RepoRoot
codex plugin add "dating-show-screenshot@dating-show-screenshot"

Write-Host "Installed dating-show-screenshot."
