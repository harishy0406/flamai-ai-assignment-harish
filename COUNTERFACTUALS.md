# Counterfactuals

These are defense prompts and rerun plans. Values are separated into measured
observations and expected effects so a defense answer does not confuse a
counterfactual with a completed experiment.

## Online FLORES access is available

**Measured result:** after Hugging Face authentication, `python partA/corpus/build_corpus.py --source flores --sample-size 250` completed and wrote the aligned corpus plus `partA/corpus/processed/manifest.json`.

**Completed rerun:**
`python partA/analysis/corrected_fertility.py --mode real`

The run produced GPT-2 and XLM-R rows for English, Hindi, Kannada, and Tamil in
`partA/analysis/results.csv` and `partA/analysis/a3_results.json`.

The final run required the project virtual environment because the global Python
installation had an incompatible `huggingface_hub==1.30.0`. The reproducible
environment pins `huggingface_hub==0.36.2` alongside Transformers.

**Decision rule:** use GPT-2/XLM-R rows only after confirming that the output metadata names the intended tokenizers and all four language files have the same non-empty line count. Keep the bundled SentencePiece result as the offline reproduction path.

## If the evaluation corpus were 10x larger

**Expected effect:** point estimates may move if the original sample was not representative, while uncertainty intervals should narrow. The tokenizer and denominator ranking should be treated as less stable if it changes materially.

**Rerun:** rebuild the corpus with the same languages and preprocessing but a 10x sample, then run `python partA/analysis/corrected_fertility.py --mode real`.

**Decision rule:** retain the routing metric only if the ranking and practical conclusion remain stable; otherwise report corpus-size sensitivity as the primary caveat.

## If the tokenizer changes

**Expected effect:** absolute fertility changes because tokenizers use different vocabularies and pre-tokenization rules. A language gap should never be attributed solely to the language until the tokenizer comparison is controlled.

**Rerun:** run `python partA/analysis/corrected_fertility.py --mode real` with the identical corpus slice.

**Decision rule:** make routing or cost recommendations from the selected production tokenizer's tokens per UTF-8 byte, while retaining grapheme-cluster results as an interpretability check.

## If the denominator changes from words to bytes or grapheme clusters

**Expected effect:** whitespace-dependent languages can look artificially worse under tokens per word. Tokens per byte better holds input payload size constant for an inference-cost comparison; grapheme clusters provide a script-aware readability check.

**Rerun:** run `python partA/analysis/corrected_fertility.py --mode real` after the corpus and tokenizer dependencies are installed.

**Decision rule:** report at least two denominators, but use one explicitly justified cost-facing denominator for the final recommendation.

## If GPU memory is 48 GB rather than 24 GB

**Expected effect:** assuming identical model weights, dtype, memory utilization, and reserve, the available KV-cache budget approximately doubles, so the estimated number of concurrent 4096-token sequences approximately doubles.

**Rerun:** substitute `GPU_mem = 48 GB` in the B1 derivation, then compare the revised ceiling with the benchmark rows.

**Decision rule:** treat this as a capacity change, not evidence that the reported throughput metric is valid; recalculate goodput from token counts and wall-clock time separately.

## If `gpu_memory_utilization` rises to 0.97

**Expected effect:** more memory becomes available to KV cache, which can reduce preemption until another bottleneck dominates. The trade-off is less headroom for runtime overhead and a higher out-of-memory risk.

**Rerun:** recompute the B1 memory budget using `GPU_mem * 0.97 - weights - reserve`, then inspect the long-context rows for the predicted shift in `kv_cache_util` and `preempted_seqs`.

**Decision rule:** approve the setting only if the reduced preemption improves true goodput without introducing instability; do not choose it from reported throughput alone.

## If the long-prompt batch size is reduced

**Expected effect:** KV-cache pressure and scheduler preemption should decrease, but aggregate throughput may also decrease. True goodput and tail latency determine whether the change is useful.

**Rerun:** execute `python partB/b3_goodput.py` for adjacent long-prompt rows, or inspect the complete `bench_log.csv` when comparing batch sizes.

**Decision rule:** select the batch size that sustains goodput while meeting the latency target and avoiding sustained preemption, rather than the row with the largest reported token rate.

## If the project helper file were deleted

**Measured dependency:** `project_inputs.py` is imported by the lowercasing audit,
missing-input audit, goodput reconciliation, and anomaly plot scripts.

**Expected effect:** deleting it would cause those commands to fail with an import
error. Keep it unless all five callers are intentionally refactored to inline the
same root/starter-kit lookup logic.

**Cleanup rule:** remove caches and raw downloads when needed, but preserve source
inputs, generated evidence, tokenizer models, and `project_inputs.py`.
