from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from project_inputs import find_input

AUDIT_INPUTS = ["fertility.py", "REPORT_v0.md"]
BENCH_INPUTS = ["bench_log.csv", "model_spec.md"]


def check_files(filenames: list[str]) -> dict[str, bool]:
    result = {}
    for name in filenames:
        try:
            find_input(name, "bench" if name in BENCH_INPUTS else None)
            result[name] = True
        except FileNotFoundError:
            result[name] = False
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["inputs", "audit", "bench"],
        default="inputs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.mode == "audit":
        result = check_files(AUDIT_INPUTS)
    elif args.mode == "bench":
        result = check_files(BENCH_INPUTS)
    else:
        result = {
            "audit": all(check_files(AUDIT_INPUTS).values()),
            "bench": all(check_files(BENCH_INPUTS).values()),
        }

    print(json.dumps(result, indent=2, sort_keys=True))

    if isinstance(result, dict) and not all(result.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
