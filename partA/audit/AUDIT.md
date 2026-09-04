# A2 Audit

The supplied starter kit contains the v0 script, report, and English/Hindi samples. The source paths resolve from either the repository root or `starter_kit/`.

### Claim: `split(" ")` over-counts words when a line contains repeated spaces

**Command:**
```bash
python partA/audit/experiments/exp_whitespace_word_count.py
```

**Before / After:**
| condition | metric | value |
|---|---|---|
| English sample, v0 | whitespace-separated fields | 79 |
| English sample, corrected | nonempty whitespace-separated words | 78 |
| Hindi sample, v0 | whitespace-separated fields | 62 |
| Hindi sample, corrected | nonempty whitespace-separated words | 61 |

**Why this proves it (1 sentence):** the token numerator is unchanged, but empty fields from repeated spaces enlarge the v0 denominator, causing a small downward distortion of tokens per word in both supplied samples.

This is a code bug, but it is not the main explanation for the report's Hindi-versus-English conclusion. Subsequent experiments separately check tokenizer choice and the suitability of tokens per word as a cross-script cost metric.

### Claim: lowercasing changes token counts for a case-sensitive tokenizer

**Command:**
```bash
python partA/audit/experiments/exp_lowercasing.py
```

**Before / After:**
| language | original tokens | lowercased tokens | changed lines |
|---|---:|---:|---:|
| English | 96 | 99 | 3 |
| Hindi | 459 | 459 | 0 |

The English sample changes under the installed GPT-2 encoding, while Hindi does not. The source-level issue is therefore demonstrated for the supplied data, and the corrected analysis must preserve original casing.

**Why this matters (1 sentence):** normalization before tokenization changes the input being measured, so the audit must preserve original casing and measure any delta rather than assuming lowercasing is neutral.

### Conceptual flaw: `tokens / word` is not a stable cross-script serving-cost metric

The v0 report treats Hindi's higher `tok/word` as direct evidence of roughly 6x serving cost. That is too strong because serving systems are billed and capacity-planned on model tokens, sequence length, KV-cache pressure, and latency, not human word counts. Word segmentation also behaves differently across scripts and languages, so `tokens / byte`, `tokens / char`, and `tokens / grapheme` should be shown next to `tokens / word` before making a routing decision.

**Corrected analysis command:**
```bash
python partA/analysis/corrected_fertility.py --mode reference
```

**Measured evidence from the bundled 250-sentence corpus:**
| tokenizer | language | tokens / word | tokens / aligned sentence |
|---|---|---:|---:|
| English-only SentencePiece | English | 4.788 | 100.904 |
| English-only SentencePiece | Hindi | 2.044 | 50.452 |
| multilingual SentencePiece | English | 5.551 | 116.996 |
| multilingual SentencePiece | Hindi | 4.806 | 118.628 |

**Why this proves it (1 sentence):** changing only the tokenizer materially changes the apparent English/Hindi relationship, so `tokens / word` alone cannot support a tokenizer-independent serving-cost claim.

### Red herring: NFC normalization is not the driver on the local corpus

**Command:**
```bash
python partA/audit/experiments/exp_nfc_red_herring.py
```

**Why this matters:** the v0 script normalizes to NFC, but the supplied starter audit samples are already NFC-normalized. If the command reports `changed=False`, normalization is not the cause of the observed fertility differences in the audited inputs. The larger FLORES corpus is checked separately when its files are used for A3.
