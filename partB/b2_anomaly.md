# B2 Throughput Anomaly

### Claim: the long-context throughput collapse starts when KV cache saturation causes scheduler preemption

**Evidence from `prompt_len=3584` rows:**

| batch | reported tok/s | KV cache utilization | preempted sequences |
|---:|---:|---:|---:|
| 16 | 1311.4 | 0.62 | 0 |
| 24 | 1607.4 | 0.93 | 0 |
| 32 | 1384.0 | 0.97 | 7 |
| 48 | 1298.5 | 0.97 | 23 |

The same rows show tail-latency deterioration: `e2e_ms_p95` rises from
`54,602.1` ms at batch 16 to `69,221.3` ms at batch 24, `97,465.7` ms at
batch 32, and `105,427.5` ms at batch 48.

The counter peaks at batch 24, then falls by 13.9% at batch 32 as cache utilization reaches 0.97 and preemption begins. At batch 48, the same saturated utilization coincides with 23 preempted sequences and a further decline. This rejects the v0 claim that throughput scales linearly with batch size.

**Configuration change:** cap long-context admission at 24 concurrent sequences (for example, with a request-admission limit or an equivalent `max_num_seqs` policy for this workload). The observed batch-24 configuration avoids preemption and has 16.1% higher reported throughput than batch 32 (`1607.4 / 1384.0 - 1`), while also avoiding the tail-latency and scheduler churn visible at higher batches. Validate the cap against output goodput and p95 latency, not only the harness counter.
