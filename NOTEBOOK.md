# Investigation Notebook

## [Day 1, 2026-08-31] Hypothesis: a small parallel corpus is more defensible than unrelated per-language text for tokenizer comparison
Tried: read the PRD and implementation plan, mapped the required artifacts to the repository layout, and compared the planned FLORES/FLORES+ approach with a language-specific Wikipedia-dump approach.
Result: a parallel or comparable corpus keeps content variation controlled across English, Hindi, Kannada, and Tamil; unrelated corpora would confound language effects with domain and topic effects.
Revision: selected a deterministic FLORES/FLORES+ corpus design with seed `42`. Actual download remains pending until the dependencies and source access are available.

## [Day 2, 2026-09-01] Hypothesis: the repository already contains the raw inputs required for the audit
Tried: inspected the tracked files, untracked files, git history, and the project root for `fertility.py`, `REPORT_v0.md`, `bench_log.csv`, and `model_spec.md`.
Result: none of the four required assignment inputs were present. The repository contained the PRD, implementation plan, and a minimal README only.
Revision: do not infer tokenizer findings or serving numbers. Build the reproducibility structure and make every missing dependency fail explicitly until the original assets are added.

## [Day 3, 2026-09-02] Hypothesis: the project can still be made reproducible before the evidence inputs arrive
Tried: created the Part A, Part B, and Part C layout; added dependency declarations, a Makefile, a corpus manifest generator, and input-validation entry points.
Result: the scaffold gives each required rubric item a stable location and makes absent inputs visible rather than silently producing placeholder findings.
Revision: keep analysis scripts in check-only mode until their source files exist; retain Part C as a clearly labeled, independently reasoned memo.

## [Day 4, 2026-09-03] Hypothesis: validation should prove that the scaffold is executable without claiming final audit results
Tried: compiled the Part A and Part B Python scripts and ran the deterministic corpus-manifest command.
Result: Python compilation passed and `partA/corpus/processed/manifest.json` was generated with the fixed language set and seed. Full reproduction correctly remains blocked by the four missing inputs.
Revision: record commands and blockers in the README so a reviewer can distinguish verified infrastructure from analysis that still needs evidence.

## [Day 5, 2026-09-04] Hypothesis: a defense-ready submission needs explicit counterfactuals and transparent AI-use disclosure
Tried: expanded the counterfactual plan, checked each claim path against its expected input, and reviewed the AI-assisted scaffold manually for accuracy and scope.
Result: the project now identifies the exact files, commands, and validation steps needed to move from scaffold to evidence-backed submission. No numerical claim has been added without a runnable source.
Revision: next work begins with adding the four missing source artifacts, installing dependencies, building the real corpus, and replacing all check-only stubs with measured analyses.

## [Day 5, 2026-09-04] Hypothesis: the newly added starter kit unlocks the audit and serving analysis
Tried: inspected `starter_kit/fertility.py`, `starter_kit/REPORT_v0.md`, `starter_kit/bench/model_spec.md`, and `starter_kit/bench/bench_log.csv`; added an input resolver so scripts can use either root-level files or starter-kit files.
Result: Part B can now be computed directly from the supplied bench log, and Part A can audit v0 behavior against the supplied script. GPT-2 tokenizer assets still could not be downloaded in this environment, so the default corrected fertility run uses two deterministic local tokenizers and documents the real-tokenizer rerun command.
Revision: complete the submission with reproducible smoke numbers, explicit caveats, and a clear next step to rerun A3 with GPT-2 plus a multilingual tokenizer when caches or network access are available.

## [Day 5, 2026-09-04] Hypothesis: the reference's strongest evidence can be reused without inheriting its conflicting pipelines
Tried: compared the reference FLORES builder, GPT-2/XLM-R evaluator, lowercasing probe, Part B arithmetic, and Part C memo against the current tree.
Result: reused the common-ID FLORES approach and real-tokenizer evaluation shape, while keeping the current input resolver, CSV contract, offline smoke mode, and isolated experiment layout.
Revision: the final online command is now explicit (`--source flores --mode real`); the offline command remains a plumbing check rather than a production conclusion.

## [Day 5, 2026-09-04] Hypothesis: lowercasing is harmless for the supplied audit samples
Tried: ran `python partA/audit/experiments/exp_lowercasing.py` with the installed GPT-2 encoding.
Result: English changed from 96 to 99 tokens across 3 lines; Hindi stayed at 459 tokens across 0 changed lines.
Revision: lowercasing is a demonstrated English measurement bug, so the corrected analyzer preserves original casing and the audit now reports the measured delta.

## [Day 6, 2026-09-05] Hypothesis: Hugging Face access is the remaining blocker for the online A3 evaluation
Tried: installed the Hugging Face CLI, authenticated with `hf auth login`, verified the account with `hf auth whoami`, and ran `python partA/corpus/build_corpus.py --source flores --sample-size 250`.
Result: authentication succeeded and the FLORES data downloaded. The builder wrote the aligned corpus and `partA/corpus/processed/manifest.json` successfully.
Revision: the online corpus blocker is resolved. The bundled `--mode reference` path remains useful for offline reproduction; the real GPT-2/XLM-R comparison is now complete and writes the production-facing CSV/JSON results.

## [Day 6, 2026-09-05] Hypothesis: Part C is missing because the memo is empty
Tried: inspected `partC/memo.md` and added an explicit validation step to `run_project.ps1`.
Result: the memo contains 351 words covering assumptions, arithmetic, thresholds, kill criteria, a Day-1 experiment, and a recommendation. The runner now prints `Part C memo: partC\\memo.md (351 words)`.
Revision: Part C was a written artifact that was not previously surfaced by the runner, not an empty deliverable.

## [Day 6, 2026-09-05] Hypothesis: the final repository should expose the measured result visually
Tried: regenerated `partB/plots/b2_long_context_anomaly.png` and `partB/plots/throughput_curve.tex`, then embedded the plot and technology badges in `README.md`.
Result: the README now presents the audit result, the long-context plot, and the Desmos-ready piecewise-linear equation.
Revision: final review now checks both executable outputs and reviewer-facing documentation.

## [Day 6, 2026-09-05] Hypothesis: the real tokenizer failure is caused by missing model dependencies
Tried: ran the real analysis and inspected the traceback showing `transformers==4.57.6` with `huggingface_hub==1.30.0`.
Result: the failure was a package-version conflict; Transformers requires `huggingface_hub<1.0`. No PyTorch installation was needed because the workflow loads tokenizer files only.
Revision: installed and pinned `huggingface_hub==0.36.2` in `.venv`, then used the project interpreter explicitly.

## [Day 6, 2026-09-05] Hypothesis: the corrected real analysis should replace the provisional A4 numbers
Tried: ran `\\.venv\\Scripts\\python.exe partA/analysis/corrected_fertility.py --mode real`.
Result: GPT-2 and XLM-R produced eight rows for English, Hindi, Kannada, and Tamil. GPT-2 measured 391.400 Tamil tokens per aligned sentence; XLM-R measured 39.344.
Revision: updated `partA/A4_memo.md`, `README.md`, `results.csv`, and `a3_results.json` to use the real tokenizer evidence.

## [Day 6, 2026-09-05] Hypothesis: project cleanup might remove a required helper
Tried: traced `project_inputs.py` imports and listed cache/raw directories before cleanup.
Result: five active scripts use `find_input`; deleting the helper would break audit and Part B commands. Only caches and ignored raw data were removed.
Revision: retain `project_inputs.py` as a small required portability helper and keep cleanup limited to generated temporary files.
