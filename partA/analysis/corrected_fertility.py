from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import regex

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUTPUT_PATH = ROOT / "partA" / "analysis" / "results.csv"
JSON_OUTPUT_PATH = ROOT / "partA" / "analysis" / "a3_results.json"
DEFAULT_CORPORA = {
    "eng": ROOT / "partA" / "corpus" / "processed" / "eng.txt",
    "hin": ROOT / "partA" / "corpus" / "processed" / "hin.txt",
    "kan": ROOT / "partA" / "corpus" / "processed" / "kan.txt",
    "tam": ROOT / "partA" / "corpus" / "processed" / "tam.txt",
}


@dataclass(frozen=True)
class TokenizerSpec:
    name: str
    encode: Callable[[str], list[int]]


def byte_tokens(text: str) -> list[int]:
    return list(text.encode("utf-8"))


def unicode_scalar_tokens(text: str) -> list[int]:
    return [ord(char) for char in text]


def load_tokenizer(name: str) -> TokenizerSpec:
    if name == "byte":
        return TokenizerSpec(name="byte", encode=byte_tokens)
    if name == "unicode_scalar":
        return TokenizerSpec(name="unicode_scalar", encode=unicode_scalar_tokens)
    if name == "gpt2":
        import tiktoken

        encoding = tiktoken.get_encoding("gpt2")
        return TokenizerSpec(name="gpt2", encode=encoding.encode)
    if name.startswith("hf:"):
        from transformers import AutoTokenizer

        model_name = name.removeprefix("hf:")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return TokenizerSpec(
            name=name,
            encode=lambda text: tokenizer.encode(text, add_special_tokens=False),
        )
    if name.startswith("spm:"):
        import sentencepiece as spm

        model_ref = name.removeprefix("spm:")
        model_paths = {
            "english_only": ROOT / "partA" / "analysis" / "models" / "english_only.model",
            "multilingual": ROOT / "partA" / "analysis" / "models" / "multilingual.model",
        }
        model_path = model_paths.get(model_ref, Path(model_ref))
        tokenizer = spm.SentencePieceProcessor(model_file=str(model_path))
        return TokenizerSpec(name=f"spm:{model_ref}", encode=lambda text: tokenizer.encode(text, out_type=int))
    raise ValueError(
        f"Unknown tokenizer {name!r}. Use byte, unicode_scalar, gpt2, hf:<model>, or spm:<model-path>."
    )


def parse_corpus_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Corpus must be LANG=PATH")
    lang, path = value.split("=", 1)
    if not lang:
        raise argparse.ArgumentTypeError("Corpus language code cannot be empty")
    return lang, Path(path)


def read_lines(path: Path) -> list[str]:
    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = unicodedata.normalize("NFC", raw_line.strip())
        if line:
            lines.append(line)
    return lines


def analyze(lang: str, path: Path, tokenizer: TokenizerSpec) -> dict[str, str | int | float]:
    lines = read_lines(path)
    token_count = 0
    word_count = 0
    byte_count = 0
    char_count = 0
    grapheme_count = 0

    for line in lines:
        token_count += len(tokenizer.encode(line))
        word_count += len(regex.findall(r"\S+", line))
        byte_count += len(line.encode("utf-8"))
        char_count += len(line)
        grapheme_count += len(regex.findall(r"\X", line))

    if not lines or word_count == 0 or byte_count == 0 or char_count == 0 or grapheme_count == 0:
        raise ValueError(f"Corpus {lang} at {path} does not contain usable text")

    return {
        "lang": lang,
        "tokenizer": tokenizer.name,
        "lines": len(lines),
        "tokens": token_count,
        "tokens_per_sentence": token_count / len(lines),
        "words": word_count,
        "bytes": byte_count,
        "chars": char_count,
        "graphemes": grapheme_count,
        "tokens_per_word": token_count / word_count,
        "tokens_per_byte": token_count / byte_count,
        "tokens_per_char": token_count / char_count,
        "tokens_per_grapheme": token_count / grapheme_count,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run corrected tokenizer fertility analysis.")
    parser.add_argument(
        "--corpus",
        action="append",
        type=parse_corpus_arg,
        help="Repeatable LANG=PATH corpus override. Defaults to partA/corpus/processed/*.txt.",
    )
    parser.add_argument(
        "--tokenizer",
        action="append",
        default=None,
        help="Repeatable tokenizer: byte, unicode_scalar, gpt2, hf:<model>, or spm:<model-path>.",
    )
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    parser.add_argument("--json-output", type=Path, default=JSON_OUTPUT_PATH)
    parser.add_argument("--mode", choices=("smoke", "reference", "real"), default="smoke")
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    corpora = dict(args.corpus or DEFAULT_CORPORA.items())
    reference_corpora = {
        "eng": ROOT / "partA" / "corpus" / "reference_flores" / "english.txt",
        "hin": ROOT / "partA" / "corpus" / "reference_flores" / "hindi.txt",
        "kan": ROOT / "partA" / "corpus" / "reference_flores" / "kannada.txt",
        "tam": ROOT / "partA" / "corpus" / "reference_flores" / "tamil.txt",
    }
    reference_tokenizers = [
        "spm:english_only",
        "spm:multilingual",
    ]
    if args.mode == "reference" and not args.corpus:
        corpora = reference_corpora
    if args.tokenizer:
        tokenizers = args.tokenizer
    elif args.mode == "reference":
        tokenizers = reference_tokenizers
    elif args.mode == "real":
        tokenizers = ["gpt2", "hf:xlm-roberta-base"]
    else:
        tokenizers = ["byte", "unicode_scalar"]
    missing = {lang: str(path) for lang, path in corpora.items() if not path.is_file()}
    if missing:
        raise SystemExit(f"Missing corpus files: {missing}")
    line_counts = {lang: len(read_lines(path)) for lang, path in corpora.items()}
    if len(set(line_counts.values())) != 1:
        raise SystemExit(f"Corpus files are not aligned: {line_counts}")

    if args.check_only:
        print(f"corpora: {', '.join(sorted(corpora))}")
        print(f"tokenizers: {', '.join(tokenizers)}")
        return

    rows = []
    for tokenizer_name in tokenizers:
        tokenizer = load_tokenizer(tokenizer_name)
        for lang, path in sorted(corpora.items()):
            rows.append(analyze(lang, path, tokenizer))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "lang",
        "tokenizer",
        "lines",
        "tokens",
        "tokens_per_sentence",
        "words",
        "bytes",
        "chars",
        "graphemes",
        "tokens_per_word",
        "tokens_per_byte",
        "tokens_per_char",
        "tokens_per_grapheme",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    payload = {
        "corpus": {
            "paths": {lang: str(path.relative_to(ROOT)) for lang, path in corpora.items()},
            "normalization": "NFC",
            "mode": args.mode,
        },
        "tokenizers": tokenizers,
        "rows": rows,
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} rows to {args.output}")
    print(f"Wrote analysis metadata to {args.json_output}")


if __name__ == "__main__":
    main()
