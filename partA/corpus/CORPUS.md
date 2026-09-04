# A1 Corpus

## Corpus

- Languages: English (`eng`), Hindi (`hin`), Kannada (`kan`), Tamil (`tam`)
- Offline source: manually curated, comparable smoke corpus in `partA/corpus/processed/*.txt`
- Final source: `facebook/flores`, `dev` split, selected by common sentence IDs
- Seed: `42`
- Offline sample size: `10` aligned/comparable sentences per language
- Recommended final sample size: `250` aligned FLORES sentences per language

## Why this source

The implementation plan calls for a small, parallel, sentence-aligned multilingual set so tokenizer comparisons can hold semantic content approximately constant across languages.

## Current state

The corpus builder writes four UTF-8 text files plus `manifest.json`. Run `python partA/corpus/build_corpus.py --source flores --sample-size 250` for the aligned evaluation corpus. Run it without `--source flores` for the offline ten-sentence smoke corpus.

The repository bundles 250 aligned sentences under
`partA/corpus/reference_flores/` so the tokenizer analysis can run offline without
depending on the gated Hugging Face dataset.

These text files are editable. Keep the same number of non-empty lines in
`english.txt`, `hindi.txt`, `kannada.txt`, and `tamil.txt` so sentence alignment remains valid.
After changing them, rerun `python partA/analysis/corrected_fertility.py --mode reference`
and treat the regenerated CSV/JSON and memo numbers as new evidence.

The corpus is intentionally small. It should be treated as a reproducibility smoke set, not as the final statistical evidence for a production tokenizer decision.

## Preprocessing

- Keep sentence alignment/comparability intact
- Preserve original Unicode text
- Normalize to NFC during analysis
- Count nonempty whitespace-delimited words with `\S+`
- Count UTF-8 bytes, Unicode scalar values, and grapheme clusters as separate denominators

## Final evidence command

```powershell
python partA/corpus/build_corpus.py --source flores --sample-size 250
python partA/analysis/corrected_fertility.py --mode real
```

FLORES mode keeps sentence alignment intact, selects sorted common IDs, preserves original Unicode text, and records checksums plus selected IDs.

## Caveats

The final write-up should explicitly cover domain mismatch between FLORES and production traffic, limited sample size, and translationese effects from parallel text. The offline smoke corpus is only 10 lines per language, so its numbers prove the pipeline and expose denominator behavior but are not production estimates.
