# bijoy-to-unicode-converter-python

Convert text typed in **Bijoy / SutonnyMJ** (an ASCII-mapped Bangla font encoding) to **Unicode Bangla**.

## Usage

```python
from bijoy_to_unicode import convertBijoyToUnicode

print(convertBijoyToUnicode('1g e‡l© `v‡Ljv cÖwµqv'))
# → ১ম বর্ষে দাখেলা প্রক্রিয়া
```

URLs and email addresses are detected and passed through unchanged so they are not chewed through by the Latin → Bangla mapping.

## Requirements

Python 3.9+. No third-party dependencies — only the standard library `re`.

## How it works

`convertBijoyToUnicode` runs five passes:

1. URL/email masking — protects ASCII tokens from the Latin → Bangla mapping.
2. Pre-normalization — collapses double kars, hoshonto+kar collisions, whitespace.
3. Main glyph map — Bijoy code points → Bangla code points / pre-composed conjunct sequences.
4. Reorder — reph relocation, halant-after-kar swap, RA-halant-kar swap, pre-kar walk past consonant clusters (combining `ে + া → ো` and `ে + ৗ → ৌ`), nukta after kar.
5. Post-fixups — `ঃ` after digits → `:`, PDF Symbol-font bullets → `•`, URL/email un-masking.

Each reorder helper is a single left-to-right walk with explicit index advancement so a transform never re-fires on a slot it just rewrote.

## Scope and caveats

- The glyph map is tuned for **SutonnyMJ**, the most common Bijoy font. Older Sutonny variants assign a few code points to different conjuncts (`Í`, `ø`, `æ`, `ÿ`); processing documents authored in those fonts may need map overrides — see `CLAUDE.md`.
- Source typos pass through verbatim. If the original typist hit `KZ…K©` (yielding `কতৃর্ক`) when they meant `K©Z…K` (`কর্তৃক`), the output reflects the source. The converter does not second-guess input.

## Credits

The original glyph map and reorder logic are derived from the long-standing community PHP/Python Bijoy converter (see `mad-fox/bijoy2unicode` and predecessors). Documented fixes in this fork: a bytes-vs-str bug that silently no-op'd the reorder pass, four SutonnyMJ-specific glyph-map corrections, single-pass reorder helpers, and URL/email passthrough.
