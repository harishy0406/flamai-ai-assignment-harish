"""Resolve assignment inputs from either the repository root or starter kit."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def find_input(name: str, section: str | None = None) -> Path:
    """Return an input path, preferring a user-supplied root-level file."""
    candidates = [ROOT / name, ROOT / "starter_kit" / name]
    if section:
        candidates.append(ROOT / "starter_kit" / section / name)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = ", ".join(str(candidate.relative_to(ROOT)) for candidate in candidates)
    raise FileNotFoundError(f"Could not find {name}. Searched: {searched}")
