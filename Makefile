PYTHON ?= python

.PHONY: corpus audit analysis bench partc reproduce check-inputs

corpus:
	$(PYTHON) partA/corpus/build_corpus.py

audit:
	$(PYTHON) partA/audit/experiments/exp_missing_inputs.py --mode audit
	$(PYTHON) partA/audit/experiments/exp_whitespace_word_count.py
	$(PYTHON) partA/audit/experiments/exp_lowercasing.py
	$(PYTHON) partA/audit/experiments/exp_nfc_red_herring.py

analysis:
	$(PYTHON) partA/analysis/corrected_fertility.py --mode reference

bench:
	$(PYTHON) partB/b3_goodput.py --batch-size 24 --prompt-len 3584
	$(PYTHON) partB/plot_anomaly.py

partc:
	$(PYTHON) -c "from pathlib import Path; p=Path('partC/memo.md'); assert p.is_file() and p.stat().st_size > 0; print('Part C memo present')"

check-inputs:
	$(PYTHON) partA/audit/experiments/exp_missing_inputs.py --mode inputs

reproduce: check-inputs corpus audit analysis bench partc
