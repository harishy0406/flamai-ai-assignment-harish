from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from project_inputs import find_input


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure the v0 lowercasing effect.")
    parser.add_argument("--tokenizer", default="gpt2")
    args = parser.parse_args()

    import tiktoken

    encoding = tiktoken.get_encoding(args.tokenizer)
    for language, filename in (("eng", "eng_sample.txt"), ("hin", "hin_sample.txt")):
        path = find_input(filename, "corpus_sample")
        lines = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        original = [len(encoding.encode(line)) for line in lines]
        lowercased = [len(encoding.encode(line.lower())) for line in lines]
        changed = sum(before != after for before, after in zip(original, lowercased))
        print(
            f"{language}: original_tokens={sum(original)} "
            f"lowercased_tokens={sum(lowercased)} "
            f"changed_lines={changed}"
        )


if __name__ == "__main__":
    main()