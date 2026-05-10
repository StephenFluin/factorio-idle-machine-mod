#!/usr/bin/env python3
"""Build a clean distributable archive for this Factorio mod."""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
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

REQUIRED_RELEASE_FILES = (
    "info.json",
    "data.lua",
    "control.lua",
)


def load_mod_metadata() -> tuple[str, str]:
    with INFO_PATH.open("r", encoding="utf-8") as f:
        info = json.load(f)

    mod_name = info.get("name")
    mod_version = info.get("version")

    if not mod_name or not mod_version:
        raise ValueError("info.json must contain both 'name' and 'version'.")

    return mod_name, mod_version


def expected_archive_name() -> str:
    mod_name, mod_version = load_mod_metadata()
    return f"{mod_name}_{mod_version}.zip"


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


def validate_release_files(files: list[Path]) -> None:
    included = {path.relative_to(REPO_ROOT).as_posix() for path in files}

    missing_required = [name for name in REQUIRED_RELEASE_FILES if name not in included]
    if missing_required:
        missing_text = ", ".join(missing_required)
        raise RuntimeError(f"Missing required release files: {missing_text}")

    if "LICENSE" not in included:
        print(
            "Warning: LICENSE not found in package contents. "
            "Adding a plaintext LICENSE is strongly recommended for mod portal releases.",
            file=sys.stderr,
        )

    if "thumbnail.png" not in included:
        print(
            "Warning: thumbnail.png not found in package contents. "
            "Adding one is recommended for better mod portal presentation.",
            file=sys.stderr,
        )


def build_archive(output_name: str) -> Path:
    files = gather_files(output_name)

    if not files:
        raise RuntimeError("No files selected for packaging.")

    validate_release_files(files)

    output_path = REPO_ROOT / output_name
    root_in_zip = output_path.stem

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as zf:
        for file_path in files:
            rel = file_path.relative_to(REPO_ROOT).as_posix()
            arcname = f"{root_in_zip}/{rel}"
            zf.write(file_path, arcname)

    return output_path


def parse_args() -> argparse.Namespace:
    default_output = expected_archive_name()

    parser = argparse.ArgumentParser(
        description=(
            "Build a distributable Factorio mod zip from this repository, "
            "excluding development and repository files."
        )
    )
    parser.add_argument(
        "--output",
        default=default_output,
        help=f"Output zip filename (default: {default_output})",
    )
    args = parser.parse_args()

    expected = expected_archive_name()
    if args.output != expected:
        raise ValueError(
            f"Output filename must match Factorio release format from info.json: {expected}"
        )

    return args


def main() -> int:
    args = parse_args()
    output_path = build_archive(args.output)
    print(f"Built {output_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
