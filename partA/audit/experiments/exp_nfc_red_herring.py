from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PATHS = [
    ROOT / "starter_kit" / "corpus_sample" / "eng_sample.txt",
    ROOT / "starter_kit" / "corpus_sample" / "hin_sample.txt",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether NFC normalization changes corpus text.")
    parser.add_argument("paths", nargs="*", type=Path, default=DEFAULT_PATHS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.paths:
        text = path.read_text(encoding="utf-8")
        normalized = unicodedata.normalize("NFC", text)
        changed_chars = sum(left != right for left, right in zip(text, normalized))
        length_delta = len(normalized) - len(text)
        print(
            f"{path.name}: changed={text != normalized} "
            f"changed_positions={changed_chars} length_delta={length_delta}"
        )


if __name__ == "__main__":
    main()
