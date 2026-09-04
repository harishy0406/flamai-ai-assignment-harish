# A4 Memo

## Corrected Headline

The v0 recommendation is too confident. The final evidence uses 250 aligned
sentences with GPT-2 and XLM-R. The decision-facing primary metric is tokens per
aligned sentence because each row represents the same translation unit:

| tokenizer | English | Hindi | Kannada | Tamil |
|---|---:|---:|---:|---:|
| GPT-2 | 26.204 | 189.472 | 346.220 | 391.400 |
| XLM-R | 29.540 | 37.048 | 40.020 | 39.344 |

These are aggregate tokens per aligned sentence from the 250-sentence FLORES
corpus. The command is `python partA/analysis/corrected_fertility.py --mode real`.

GPT-2 fragments Indic text dramatically more than English, while XLM-R keeps all
four languages within a much narrower range. For GPT-2, Tamil is approximately
`14.9x` English by tokens per aligned sentence; for XLM-R, Kannada is only
`1.36x` English. This demonstrates why tokenizer choice must be specified before
making a routing claim.

## Recommendation

Do not route all Indic traffic to a separate model only from the v0 fertility table. If production uses GPT-2-like tokenization, Indic traffic needs materially more token budget; if production uses XLM-R-like tokenization, the gap is much smaller. Decide using the production tokenizer's tokens per request together with latency, quality, and cache pressure.

## Biggest Caveat

The online GPT-2/XLM-R run is now complete using authenticated Hugging Face access. The bundled local SentencePiece run remains available as an offline reproduction path.

```bash
python partA/analysis/corrected_fertility.py --mode reference
```

## Production Monitoring Metric

Track `tokens_per_successful_request` by language and production tokenizer, with p50/p95 latency, KV-cache utilization, preemption rate, and refusal/error rate attached.
