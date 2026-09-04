"""Measure the v0 word-count distortion caused by repeated spaces."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def counts(path: Path) -> tuple[int, int]:
    v0_count = 0
    corrected_count = 0
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        v0_count += len(line.split(" "))
        corrected_count += len(line.split())
    return v0_count, corrected_count


def main() -> None:
    for language in ("eng", "hin"):
        path = ROOT / "starter_kit" / "corpus_sample" / f"{language}_sample.txt"
        v0_count, corrected_count = counts(path)
        inflation = (v0_count / corrected_count - 1) * 100
        print(
            f"{language}: v0_words={v0_count}, corrected_words={corrected_count}, "
            f"denominator_inflation={inflation:.2f}%"
        )


if __name__ == "__main__":
    main()
