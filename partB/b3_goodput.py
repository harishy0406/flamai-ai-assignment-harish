from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_inputs import find_input


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reconcile reported throughput with output-token goodput."
    )
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--batch-size", type=int, default=24)
    parser.add_argument("--prompt-len", type=int, default=3584)
    return parser.parse_args()


def load_row(batch_size: int, prompt_len: int) -> dict[str, str]:
    path = find_input("bench_log.csv", "bench")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if int(row["batch_size"]) == batch_size and int(row["prompt_len"]) == prompt_len:
            return row
    raise ValueError(f"No row for batch_size={batch_size}, prompt_len={prompt_len}")


def calculate(row: dict[str, str]) -> dict[str, float]:
    batch = int(row["num_requests"])
    prompt = int(row["prompt_len"])
    generated = int(row["gen_len"])
    wall_clock = float(row["wall_clock_s"])
    reported = float(row["reported_tok_s"])
    e2e_p95 = float(row["e2e_ms_p95"]) / 1000
    return {
        "reported_formula_tok_s": (prompt + generated) * batch / wall_clock,
        "reported_tok_s": reported,
        "output_goodput_wall_clock_tok_s": generated * batch / wall_clock,
        "output_tokens_per_e2e_p95_s": generated * batch / e2e_p95,
        "prompt_share_of_reported": prompt / (prompt + generated),
    }


def main() -> None:
    args = parse_args()
    if args.check_only:
        print(find_input("bench_log.csv", "bench"))
        print(find_input("model_spec.md", "bench"))
        return

    row = load_row(args.batch_size, args.prompt_len)
    metrics = calculate(row)
    print(f"source_row: batch={args.batch_size}, prompt_len={args.prompt_len}")
    for name, value in metrics.items():
        print(f"{name}: {value:.3f}")
    if abs(metrics["reported_formula_tok_s"] - metrics["reported_tok_s"]) > 0.2:
        raise SystemExit("reported throughput does not match prompt-plus-output formula")


if __name__ == "__main__":
    main()
