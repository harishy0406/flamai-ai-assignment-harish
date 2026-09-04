# B1 KV-Cache Ceiling

For FP16 KV cache, one token stores both K and V for every layer:

```text
bytes/token = 2 * layers * KV heads * head dimension * bytes/element
            = 2 * 28 * 8 * 128 * 2
            = 114,688 bytes (112 KiB)
```

Using the model spec's decimal GB units:

```text
usable GPU memory = 24.0 GB * 0.92 = 22.08 GB
weights           = 4.2 B parameters * 2 bytes = 8.40 GB
runtime reserve   = 1.60 GB
KV budget         = 22.08 - 8.40 - 1.60 = 12.08 GB

4096-token sequence KV footprint = 4,096 * 114,688 = 469,762,048 bytes
theoretical concurrent sequences  = 12.08e9 / 469,762,048 = 25.7
```

This predicts a practical ceiling near 24 to 25 full-length sequences after allocator fragmentation and safety margin. The log is consistent: the batch-24, 3584-token-prompt row reaches `kv_cache_util=0.93` without preemption, while batch 32 reaches `0.97` and preempts 7 sequences. The calculation is an estimate, because the 1.6 GB non-KV reserve is explicitly approximate and request generation length increases KV occupancy during decoding.
