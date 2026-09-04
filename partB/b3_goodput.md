# B3 Goodput Reconciliation

### Claim: `reported_tok_s` is prompt-plus-output throughput, not output goodput

**Command:**
```bash
python partB/b3_goodput.py --batch-size 24 --prompt-len 3584
```

**Before / After:**

| quantity | calculation | value (tok/s) |
|---|---|---:|
| harness counter | reported by CSV | 1607.4 |
| reconstructed counter | `(3584 + 512) * 24 / 61.16` | 1607.3 |
| output goodput | `512 * 24 / 61.16` | 200.9 |
| latency-normalized output indicator | `512 * 24 / 69.2213` | 177.6 |

**Why this proves it:** the reconstructed counter matches the CSV only when the 3584 prompt tokens are included; 87.5% of that counter is prompt work rather than generated output.

The wall-clock result is the exact aggregate output goodput for the run. The latency result divides total output tokens by p95 end-to-end latency, so it is a conservative latency-normalized indicator, not an independent aggregate-goodput measurement. It is useful for showing tail-latency pressure, but it must not be presented as a second exact throughput derivation.

The v0 report should say that the batch-24 long-prompt run produced approximately 201 output tokens/s end-to-end, while its 1607 tok/s harness counter includes prompt processing. It should not extrapolate batch-48 throughput linearly: the log records 1298.5 reported tok/s at batch 48, with 23 preempted sequences.
