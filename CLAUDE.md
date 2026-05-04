# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repo shape

Single-file library: `bijoy_to_unicode.py`. No dependencies beyond the standard library `re`. Public entry: `convertBijoyToUnicode(srcString) -> str`.

The glyph map and reorder passes assume the **SutonnyMJ** Bijoy font, the most common variant. Other Bijoy fonts (e.g. older Sutonny64) reuse some code points for different conjuncts — see "Glyph map is font-specific" below before processing different documents.

## Conversion pipeline

`convertBijoyToUnicode` runs five passes — order matters:

1. **`_protect_ascii_runs`** — masks URLs (`http(s)://…`, `www.…`, `ftp://…`) and emails with single-codepoint Private-Use-Area sentinels so they survive the Latin→Bangla mapping; restored at the end.
2. **`doCharMap(s, preConversionMap)`** — regex-based normalization of Bijoy-side typing artefacts (double kars, hoshonto+kar collisions, whitespace).
3. **`doCharMap(s, conversionMap)`** — main glyph→Unicode substitution: vowels, consonants, digits, kars, jukto-okkhor (single-glyph conjunct ligatures expanded to halant sequences).
4. **`reArrangeUnicodeConvertedText`** — six small single-pass walks, each with explicit index advancement so transforms never re-fire on relocated chars:
   - `_move_reph` — `র + halant` (Bijoy's reph at end of cluster) is moved to the start of the cluster it belongs to.
   - `doCharMap(s, proConversionMap)` — collapses `্্` → `্`.
   - `_swap_halant_after_kar` — `kar/nukta + halant + consonant` → `halant + consonant + kar`.
   - `_swap_ra_halant_kar` — `র + halant + kar` (no halant before `র`) → `kar + র + halant`.
   - `_move_pre_kars` — pre-kars (`ি`, `ৈ`, `ে`) walk past the following consonant cluster. Combines `ে + া` → `ো` and `ে + ৗ` → `ৌ` across the cluster boundary.
   - `_move_nukta_after_kar` — `nukta + post-kar` → `post-kar + nukta`.
5. **`doCharMap(s, postConversionMap)`** — fix-ups (`ঃ` after digit/space → `:`, PUA bullets → `•`, etc.) and the URL/email un-masking.

There is no `refactor_broken_kars` final pass — it was a band-aid for the older broken reorder pass and would corrupt correctly-ordered output now.

## Things to know before changing code

- **`mb_substr` / `mbCharAt` return `str`.** They used to return `bytes` (encoded UTF-8) which silently failed every comparison against `str` literals (`'র'`, `'্'`), making the entire reorder pass a no-op. Changing them back to `bytes` would resurrect that bug.
- **`doCharMap` keys are regex.** Map entries with regex metacharacters are pre-escaped in the source (`'\\|'`, `'\\&'`, `'\\^'`, `'\\['`). Adding new entries with `.`, `*`, `+`, `?`, `()`, `[]`, `{}`, `|`, `\`, `^`, `$` requires the same escaping.
- **`preConversionMap` ordering matters.** It relies on Python dict insertion order (3.7+); reordering can change behavior (e.g. `' +'` collapse must run before whitespace-around-punct rules).
- **Glyph map is font-specific.** The current values for `Í → ত`, `ø → ্ল`, `æ → ু`, `ÿ → ক্ষ` are correct for **SutonnyMJ**. Older Sutonny variants assign these slots to `ত্ম`, `স্ন`, `ম্ন`, etc. — process other-font documents at your own risk and verify a sample first.
- **Sentinels live in `…`** (PUA). `_protect_ascii_runs` assumes ≤256 protected runs per call. Bump the encoding if you ever need more.
- The reorder helpers (`_move_reph`, `_move_pre_kars`, …) are intentionally separate single-pass walks. Combining them or moving to a multi-condition `for` loop will reintroduce the "transform fires twice on the same relocated char" bug that produced things like `প্রক্রয়াি` and `উল্লখে`.

## Working on the conversion logic

- **No automated tests in repo.** Verify with sample words against a live document before/after any change. Sanity-check NFC equivalence (`unicodedata.normalize('NFC', got) == NFC(expected)`) — the converter emits precomposed `য়`/`ড়` while many test strings are decomposed.
- The maps encode behavior. Prefer adding map entries over adding code branches.
- If you spot a new Bijoy variant glyph that the map doesn't handle, add it as a single map entry rather than special-casing in the reorder pass.

## PDF extraction note

If you build a pipeline that feeds PDF-extracted Bijoy text into this converter, do **not** use `pdfplumber.extract_text()` directly — it sorts overlapping glyphs by x-position and inserts spurious word-break spaces, which mangles Bijoy reph clusters (zero-width `©` glyphs that overlap the next consonant). Group `page.chars` by baseline-y instead and keep each line in PDF content-stream order; only insert a space when the x-gap exceeds half-glyph-width *and* the new glyph sits at strictly larger x than the previous one.
