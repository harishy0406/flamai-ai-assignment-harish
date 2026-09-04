# AI Usage

AI assistance was used as an industry-standard productivity tool for planning, boilerplate generation, documentation structure, and reproducibility scaffolding. I retained responsibility for the technical decisions, reviewed the output manually, and validated executable changes locally before including them.

- Task: repository scaffold and reproducibility plumbing
  AI contribution: generated the initial repository structure, Makefile targets, documentation templates, and Python script skeletons from the PRD and implementation plan.
  Manual verification and validation: inspected every generated file for consistency with the rubric, compiled the Part A and Part B scripts with Python, and ran the corpus-manifest command successfully.
  Where AI was wrong or misleading: the initial workflow implicitly assumed the assignment source files were already present. Manual repository inspection showed that `fertility.py`, `REPORT_v0.md`, `bench_log.csv`, and `model_spec.md` were absent, so I changed the implementation to surface this blocker rather than produce unsupported results.

- Task: research workflow and counterfactual preparation
  AI contribution: helped organize hypotheses, rerun commands, and documentation wording for the audit and serving analysis.
  Manual verification and validation: checked that counterfactuals distinguish expected behavior from measured results and that no numerical audit claim is presented without the corresponding source input and runnable analysis.
  Where AI was wrong or misleading: generic recommendations can sound conclusive even when they depend on model configuration, tokenizer choice, or benchmark rows. I therefore kept these items conditional and tied each one to a concrete rerun or decision rule.

AI did not replace analysis of the supplied artifacts. After the starter kit was added, I reran the relevant scripts locally, checked generated CSV/manifest outputs, and manually validated that the written conclusions matched the measured commands and known caveats.

- Task: integrate reusable evidence from the reference project
  AI contribution: proposed reusing the common-ID FLORES builder, tokenizer evaluation structure, and lowercasing probe without copying the reference repository wholesale.
  Manual verification and validation: kept the current repository layout, renamed the copied models to `english_only.model` and `multilingual.model`, regenerated the 250-sentence CSV/JSON outputs, and removed the obsolete `reference_project` directory.
  Where AI was wrong or misleading: changing dataset names did not solve access. Both `facebook/flores` and `openlanguagedata/flores_plus` returned gated-access errors, so the project retained a bundled offline corpus and documented Hugging Face authentication as a prerequisite.

- Task: serving visualization and reproducibility polish
  AI contribution: added the Desmos equation generator, corrected the multi-axis anomaly plot, updated the PowerShell runner, README, and gitignore.
  Manual verification and validation: reran `run_project.ps1 -SkipInstall`, checked `throughput_curve.tex`, ran Ruff and `compileall`, and verified that the runner stops on failures and reports the Part C memo.
  Where AI was wrong or misleading: an early plot placed preemption counts and KV utilization on the same `0..1.1` axis, clipping counts up to 23. Review found the issue and replaced it with a third axis.

- Task: authenticated final corpus run
  AI contribution: provided the Hugging Face CLI setup and online corpus commands.
  Manual verification and validation: `hf auth whoami` reported the authenticated user, and `python partA/corpus/build_corpus.py --source flores --sample-size 250` completed successfully, generating the corpus manifest and aligned files.
  Where AI was wrong or misleading: the initial `hf` command was unavailable because the CLI executable was not on PATH even though `huggingface_hub` was installed. The working solution installed the CLI extra and added the Python user Scripts directory to the current PowerShell PATH.

- Task: diagnose the failed real tokenizer run
  AI contribution: identified the dependency conflict from the traceback and recommended using the project virtual environment.
  Manual verification and validation: installed `huggingface_hub==0.36.2` in `.venv`, verified `transformers==4.57.6` imports successfully, and reran `\.venv\\Scripts\\python.exe partA/analysis/corrected_fertility.py --mode real` with exit code 0.
  Where AI was wrong or misleading: the first command used the global Python installation, which had `huggingface_hub==1.30.0` and was incompatible with Transformers. The fix was to pin the compatible dependency and use `.venv`, not to install PyTorch.

- Task: final cleanup and documentation
  AI contribution: updated README commands/results and identified removable caches.
  Manual verification and validation: updated the README with the measured GPT-2/XLM-R table, retained `project_inputs.py` because five active scripts import it, and removed only `.ruff_cache`, `.pytest_cache`, `__pycache__`, and the ignored raw corpus cache.
