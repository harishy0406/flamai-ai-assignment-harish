# B4 Monitoring Metric

Monitor scheduler preemption rate together with KV-cache block utilization. For the long-context workload, the log shows the expected confirmation pattern: utilization rises from 0.93 at batch 24 with zero preemptions to 0.97 at batch 32 with 7 preemptions and remains at 0.97 at batch 48 with 23 preemptions. Alert when utilization is sustained near 0.97 and preemption is nonzero, because that combination confirms cache pressure rather than healthy batching; use the alert to lower admission concurrency before output goodput and tail latency deteriorate.
