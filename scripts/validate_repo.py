#!/usr/bin/env python3
"""Validate the repository layout without requiring a local Codex installation."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "dating-show-screenshot"
SKILL_ROOT = PLUGIN_ROOT / "skills" / "make-dating-show-screenshot"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain an object")
    return payload


def validate_plugin() -> None:
    manifest = load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")
    required = {"name", "version", "description", "author", "skills", "interface"}
    missing = required - set(manifest)
    assert not missing, f"plugin.json missing: {sorted(missing)}"
    assert manifest["name"] == "dating-show-screenshot"
    assert SEMVER.fullmatch(manifest["version"])
    assert manifest["skills"] == "./skills/"
    interface = manifest["interface"]
    for key in [
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "defaultPrompt",
    ]:
        assert interface.get(key), f"plugin interface missing {key}"
    for relative in [
        interface["composerIcon"],
        interface["logo"],
        *interface["screenshots"],
    ]:
        assert relative.startswith("./assets/")
        assert (PLUGIN_ROOT / relative).is_file(), f"missing plugin asset: {relative}"


def validate_skill() -> None:
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    frontmatter_text = text.split("---", 2)[1]
    frontmatter = yaml.safe_load(frontmatter_text)
    assert frontmatter["name"] == "make-dating-show-screenshot"
    assert "description" in frontmatter
    assert "[TODO:" not in text
    for path in SKILL_ROOT.rglob("*"):
        assert "[TODO:" not in path.name


def validate_marketplace() -> None:
    marketplace = load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    entry = next(
        item for item in marketplace["plugins"] if item["name"] == "dating-show-screenshot"
    )
    assert entry["source"] == {
        "source": "local",
        "path": "./plugins/dating-show-screenshot",
    }
    assert entry["policy"]["installation"] == "AVAILABLE"
    assert entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}
    assert entry["category"] == "Creativity"


def main() -> None:
    validate_plugin()
    validate_skill()
    validate_marketplace()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
