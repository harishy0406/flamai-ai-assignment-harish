from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from project_inputs import find_input

OUTPUT_PATH = ROOT / "partB" / "plots" / "b2_long_context_anomaly.png"
EQUATION_PATH = ROOT / "partB" / "plots" / "throughput_curve.tex"


def throughput_equation(batches: list[int], throughput: list[float]) -> str:
    pieces = []
    for left, right, left_value, right_value in zip(
        batches[:-1], batches[1:], throughput[:-1], throughput[1:]
    ):
        slope = (right_value - left_value) / (right - left)
        intercept = left_value - slope * left
        pieces.append(
            f"{slope:.6f}x{intercept:+.6f} & {left}\\le x\\le {right}"
        )
    return "y=\\left\\{\\begin{array}{ll}" + "\\\\".join(pieces) + "\\end{array}\\right."


def main() -> None:
    source = find_input("bench_log.csv", "bench")
    with source.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if int(row["prompt_len"]) == 3584
        ]

    batches = [int(row["batch_size"]) for row in rows]
    throughput = [float(row["reported_tok_s"]) for row in rows]
    cache_util = [float(row["kv_cache_util"]) for row in rows]
    preemptions = [int(row["preempted_seqs"]) for row in rows]

    fig, primary = plt.subplots(figsize=(8, 4.5))
    primary.plot(batches, throughput, marker="o", color="#1b5e20", label="Reported tok/s")
    primary.set_xlabel("Batch size")
    primary.set_ylabel("Reported tok/s", color="#1b5e20")
    primary.tick_params(axis="y", labelcolor="#1b5e20")
    primary.set_xticks(batches)
    primary.grid(axis="y", alpha=0.25)

    secondary = primary.twinx()
    secondary.plot(batches, cache_util, marker="s", color="#b71c1c", label="KV cache utilization")
    secondary.set_ylabel("KV cache utilization", color="#b71c1c")
    secondary.set_ylim(0, 1.1)
    tertiary = primary.twinx()
    tertiary.spines["right"].set_position(("axes", 1.12))
    tertiary.bar(batches, preemptions, width=2, color="#ef6c00", alpha=0.45, label="Preempted sequences")
    tertiary.set_ylabel("Preempted sequences", color="#ef6c00")
    tertiary.set_ylim(0, max(preemptions) + 4)

    lines, labels = primary.get_legend_handles_labels()
    right_lines, right_labels = secondary.get_legend_handles_labels()
    third_lines, third_labels = tertiary.get_legend_handles_labels()
    primary.legend(lines + right_lines + third_lines, labels + right_labels + third_labels, loc="lower left")
    fig.tight_layout()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH, dpi=160)
    equation = throughput_equation(batches, throughput)
    EQUATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    EQUATION_PATH.write_text(equation + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    print("Desmos LaTeX equation for reported throughput:")
    print(equation)
    print(f"Saved equation to {EQUATION_PATH}")


if __name__ == "__main__":
    main()
