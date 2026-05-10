#!/usr/bin/env python3
"""Build a clean distributable archive for this Factorio mod."""

from __future__ import annotations

import argparse
import fnmatch
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parent
INFO_PATH = REPO_ROOT / "info.json"

EXCLUDE_PATTERNS = (
    ".git/**",
    ".github/**",
    ".gemini/**",
    "dist/**",
    "__pycache__/**",
    ".vscode/**",
    ".idea/**",
    "*.md",
    "*.py",
    "*.js",
    "screenshot*.png",
    "*.zip",
    ".gitignore",
)


def load_mod_metadata() -> tuple[str, str]:
    with INFO_PATH.open("r", encoding="utf-8") as f:
        info = json.load(f)

    mod_name = info.get("name")
    mod_version = info.get("version")

    if not mod_name or not mod_version:
        raise ValueError("info.json must contain both 'name' and 'version'.")

    return mod_name, mod_version


def should_exclude(path: Path, output_file_name: str) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()

    if rel == output_file_name:
        return True

    if path.name == "build_mod.py":
        return True

    for pattern in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True

    return False


def gather_files(output_file_name: str) -> list[Path]:
    files: list[Path] = []

    for path in REPO_ROOT.rglob("*"):
        if path.is_dir():
            continue

        if should_exclude(path, output_file_name):
            continue

        files.append(path)

    return sorted(files)


def build_archive(output_name: str) -> Path:
    mod_name, mod_version = load_mod_metadata()
    root_in_zip = f"{mod_name}_{mod_version}"
    files = gather_files(output_name)

    if not files:
        raise RuntimeError("No files selected for packaging.")

    output_path = REPO_ROOT / output_name

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as zf:
        for file_path in files:
            rel = file_path.relative_to(REPO_ROOT).as_posix()
            arcname = f"{root_in_zip}/{rel}"
            zf.write(file_path, arcname)

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a distributable Factorio mod zip from this repository, "
            "excluding development and repository files."
        )
    )
    parser.add_argument(
        "--output",
        default="idle-machine.zip",
        help="Output zip filename (default: idle-machine.zip)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = build_archive(args.output)
    print(f"Built {output_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
