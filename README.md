# bijoy-to-unicode-converter-python

[![Try it in your browser](https://img.shields.io/badge/Try_it-online_demo-1f6feb?style=for-the-badge)](https://rabiulislam-xyz.github.io/bijoy-to-unicode-converter-python/)

Convert text typed in **Bijoy / SutonnyMJ** (an ASCII-mapped Bangla font encoding) to **Unicode Bangla**.

Paste Bijoy text and see Unicode output instantly in [the live demo](https://rabiulislam-xyz.github.io/bijoy-to-unicode-converter-python/) — runs entirely in your browser via Pyodide, nothing is uploaded.

## Usage

```python
from bijoy_to_unicode import convertBijoyToUnicode

bijoy = """cvwievwiK Drm‡e Zvwjeyj Bj‡gi AskMÖnY Kvg¨ n‡j, Zvi ZvwiL Zvwjeyj Bj‡gi mgqm~Px jÿ¨ †i‡L
Ki‡Z n‡e| (Ab¨_vq welqwU Zvwjeyj Bj‡gi A‡MvP‡i ivL‡Z n‡e|) GB †¶‡Î †Kvb cÖKvi Av‡e`b
Kivi my‡hvM _vK‡e bv|
c„ôv bs - 3"""

print(convertBijoyToUnicode(bijoy))
# পারিবারিক উৎসবে তালিবুল ইলমের অংশগ্রহণ কাম্য হলে, তার তারিখ তালিবুল ইলমের সময়সূচী লক্ষ্য রেখে
# করতে হবে। (অন্যথায় বিষয়টি তালিবুল ইলমের অগোচরে রাখতে হবে।) এই ক্ষেত্রে কোন প্রকার আবেদন
# করার সুযোগ থাকবে না।
# পৃষ্ঠা নং - ৩
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
