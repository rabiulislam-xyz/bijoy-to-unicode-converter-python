import re


def mb_substr(s, start, length=None, encoding="UTF-8"):
    """Return a slice of ``s`` as ``str``.

    The original code returned ``bytes`` (encoded UTF-8); callers compare the
    result against ``str`` literals like ``'র'`` and ``'\\u09CD'``, so the
    bytes form silently failed every comparison and the reorder pass became
    a no-op. ``encoding`` is kept for signature compatibility but unused.
    """
    if length is None:
        return s[start:]
    return s[start:start + length]


preConversionMap = {
    ' +': ' ',
    'yy': 'y',  # Double Hrosh-u-Kar
    'vv': 'v',  # Double Aa-Kar
    '­­': '­',  # Double Jukto-L - L+Double-L = Triple L
    'y&': 'y',  # Hoshonto+Hrosh-u
    '„&': '„',  # Hoshonto+Ri-Kar
    '‡u': 'u‡',  # ChondroBindu Error /Typing Mistake
    'wu': 'uw',  # ChondroBindu Error /Typing Mistake
    ' ,': ',',
    ' \\|': '\\|',
    '\\\\ ': '',
    ' \\\\': '',
    '\\\\': '',
    '\n +': '\n',
    ' +\n': '\n',
    '\n\n\n\n\n': '\n\n',
    '\n\n\n\n': '\n\n',
    '\n\n\n': '\n\n'
}

conversionMap = {
    # Vowels Start
    'Av': 'আ',
    'A': 'অ',
    'B': 'ই',
    'C': 'ঈ',
    'D': 'উ',
    'E': 'ঊ',
    'F': 'ঋ',
    'G': 'এ',
    'H': 'ঐ',
    'I': 'ও',
    'J': 'ঔ',
    # Constants
    'K': 'ক',
    'L': 'খ',
    'M': 'গ',
    'N': 'ঘ',
    'O': 'ঙ',
    'P': 'চ',
    'Q': 'ছ',
    'R': 'জ',
    'S': 'ঝ',
    'T': 'ঞ',
    'U': 'ট',
    'V': 'ঠ',
    'W': 'ড',
    'X': 'ঢ',
    'Y': 'ণ',
    'Z': 'ত',
    '_': 'থ',
    '`': 'দ',
    'a': 'ধ',
    'b': 'ন',
    'c': 'প',
    'd': 'ফ',
    'e': 'ব',
    'f': 'ভ',
    'g': 'ম',
    'h': 'য',
    'i': 'র',
    'j': 'ল',
    'k': 'শ',
    'l': 'ষ',
    'm': 'স',
    'n': 'হ',
    'o': 'ড়',
    'p': 'ঢ়',
    'q': 'য়',
    'r': 'ৎ',
    's': 'ং',
    't': 'ঃ',
    'u': 'ঁ',
    # Numbers
    '0': '০',
    '1': '১',
    '2': '২',
    '3': '৩',
    '4': '৪',
    '5': '৫',
    '6': '৬',
    '7': '৭',
    '8': '৮',
    '9': '৯',
    # Kars
    '•': 'ঙ্',
    'v': 'া',  # Aa-Kar
    'w': 'ি',  # i-Kar
    'x': 'ী',  # I-Kar
    'y': 'ু',  # u-Kar
    'z': 'ু',  # u-Kar
    '“': 'ু',  # u-kar
    '–': 'ু',  # u-kar
    '~': 'ূ',  # U-kar
    'ƒ': 'ূ',  # U-kaar
    '‚': 'ূ',  # U-kaar
    '„„': 'ৃ',  # Double Rri-kar Bug
    '„': 'ৃ',  # Ri-Kar
    '…': 'ৃ',  # Ri-Kar
    '†': 'ে',  # E-Kar
    '‡': 'ে',  # E-Kar
    'ˆ': 'ৈ',  # Oi-Kar
    '‰': 'ৈ',  # Oi-Kar
    'Š': 'ৗ',  # Ou-Kar
    '\\|': '।',  # Full-Stop
    '\\&': '্‌',  # Ho-shonto
    #  Jukto Okkhor
    '\\^': '্ব',
    '‘': '্তু',
    '’': '্থ',
    '‹': '্ক',
    'Œ': '্ক্র',
    '”': 'চ্',
    '—': '্ত',
    '˜': 'দ্',
    '™': 'দ্',
    'š': 'ন্',
    '›': 'ন্',
    'œ': '্ন',
    'Ÿ': '্ব',
    '¡': '্ব',
    '¢': '্ভ',
    '£': '্ভ্র',
    '¤': 'ম্',
    '¥': '্ম',
    '¦': '্ব',
    '§': '্ম',
    '¨': '্য',
    '©': 'র্',
    'ª': '্র',
    '«': '্র',
    '¬': '্ল',
    '­': '্ল',
    '®': 'ষ্',
    '¯': 'স্',
    '°': 'ক্ক',
    '±': 'ক্ট',
    '²': 'ক্ষ্ণ',  # shu(kkhno)
    '³': 'ক্ত',
    '´': 'ক্ম',
    'µ': 'ক্র',
    '¶': 'ক্ষ',
    '·': 'ক্স',
    '¸': 'গু',
    '¹': 'জ্ঞ',
    'º': 'গ্দ',
    '»': 'গ্ধ',
    '¼': 'ঙ্ক',
    '½': 'ঙ্গ',
    '¾': 'জ্জ',
    '¿': '্ত্র',
    'À': 'জ্ঝ',
    'Á': 'জ্ঞ',
    'Â': 'ঞ্চ',
    'Ã': 'ঞ্ছ',
    'Ä': 'ঞ্জ',
    'Å': 'ঞ্ঝ',
    'Æ': 'ট্ট',
    'Ç': 'ড্ড',
    'È': 'ণ্ট',
    'É': 'ণ্ঠ',
    'Ê': 'ণ্ড',
    'Ë': 'ত্ত',
    'Ì': 'ত্থ',
    'Í': 'ত',  # SutonnyMJ glyph appears as ন্ত conjunct, but in this encoding it's
              # always written after an explicit halant-providing glyph (š=ন্, ¯=স্),
              # so emitting just ত yields the correct cluster (ন্ত, স্ত, etc.).
    'Î': 'ত্র',
    'Ï': 'দ্দ',
    'Ð': '-',
    'Ñ': '-',
    'Ò': '"',
    'Ó': '"',
    'Ô': "'",
    'Õ': "'",
    'Ö': '্র',
    '×': 'দ্ধ',
    'Ø': 'দ্ব',
    'Ù': 'দ্ম',
    'Ú': 'ন্ঠ',
    'Û': 'ন্ড',
    'Ü': 'ন্ধ',
    'Ý': 'ন্স',
    'Þ': 'প্ট',
    'ß': 'প্ত',
    'à': 'প্প',
    'á': 'প্স',
    'â': 'ব্জ',
    'ã': 'ব্দ',
    'ä': 'ব্ধ',
    'å': 'ভ্র',
    'æ': 'ু',  # SutonnyMJ "ru" ligature (post-র form of ু-kar) — used in
              # গুরু/করুন/বিরুদ্ধ/শুরু etc. The Bijoy source already has the
              # র preceding æ; emitting just ু yields the correct cluster.
    'ç': 'ম্ফ',
    'è': '্ন',
    'é': 'ল্ক',
    'ê': 'ল্গ',
    'ë': 'ল্ট',
    'ì': 'ল্ড',
    'í': 'ল্প',
    'î': 'ল্ফ',
    'ï': 'শু',
    'ÿ': 'ক্ষ',
    'ð': 'শ্চ',
    'ñ': 'শ্ছ',
    'ò': 'ষ্ণ',
    'ó': 'ষ্ট',
    'ô': 'ষ্ঠ',
    'õ': 'ষ্ফ',
    'ö': 'স্খ',
    '÷': 'স্ট',
    'ø': '্ল',  # SutonnyMJ ্ল conjunct ligature (used in আল্লাহ, উল্লেখ, গ্লাস, …)
    'ù': 'স্ফ',
    'ú': '্প',
    'û': 'হু',
    'ü': 'হৃ',
    'ý': 'হ্ন',
    'þ': 'হ্ম'
}

proConversionMap = {'্্': '্'}

postConversionMap = {
    # PDF Symbol-font private-use bullets — render them as the standard bullet.
    '': '•',
    '': '•',
    # Colon with Number/Space
    '০ঃ': '০:',
    '১ঃ': '১:',
    '২ঃ': '২:',
    '৩ঃ': '৩:',
    '৪ঃ': '৪:',
    '৫ঃ': '৫:',
    '৬ঃ': '৬:',
    '৭ঃ': '৭:',
    '৮ঃ': '৮:',
    '৯ঃ': '৯:',
    ' ঃ': ' :',
    '\nঃ': '\n:',
    ']ঃ': ']:',
    '\\[ঃ': '\\[:',
    '  ': ' ',
    'অা': 'আ',
    '্‌্‌': '্‌'
}


def IsBanglaDigit(c):
    if c >= '০' and c <= '৯':
        return True
    return False


def IsBanglaPreKar(c):
    if c == 'ি' or c == 'ৈ' or c == 'ে':
        return True
    return False


def IsBanglaPostKar(c):
    if c == 'া' or c == 'ো' or c == 'ৌ' or c == 'ৗ' or c == 'ু' or c == 'ূ' or c == 'ী' or c == 'ৃ':
        return True
    return False


def IsBanglaKar(c):
    if IsBanglaPreKar(c) or IsBanglaPostKar(c):
        return True
    return False


def IsBanglaBanjonborno(c):
    if c == 'ক' or c == 'খ' or c == 'গ' or c == 'ঘ' or c == 'ঙ' or c == 'চ' or c == 'ছ' or c == 'জ' or c == 'ঝ' or c == 'ঞ' or c == 'ট' or c == 'ঠ' or c == 'ড' or c == 'ঢ' or c == 'ণ' or c == 'ত' or c == 'থ' or c == 'দ' or c == 'ধ' or c == 'ন' or c == 'প' or c == 'ফ' or c == 'ব' or c == 'ভ' or c == 'ম' or c == 'য' or c == 'র' or c == 'ল' or c == 'শ' or c == 'ষ' or c == 'স' or c == 'হ' or c == 'ড়' or c == 'ঢ়' or c == 'য়' or c == 'ৎ' or c == 'ং' or c == 'ঃ' or c == 'ঁ':
        return True
    return False


def IsBanglaSoroborno(c):
    if c == 'অ' or c == 'আ' or c == 'ই' or c == 'ঈ' or c == 'উ' or c == 'ঊ' or c == 'ঋ' or c == 'ঌ' or c == 'এ' or c == 'ঐ' or c == 'ও' or c == 'ঔ':
        return True
    return False


def IsBanglaNukta(c):
    if c == 'ঁ':
        return True
    return False


def IsBanglaHalant(c):
    if c == '্':
        return True
    return False


def IsSpace(c):
    if c == ' ' or c == '\t' or c == '\n' or c == '\r':
        return True
    return False


def _at(s, i):
    """Safe single-char access — returns '' for out-of-bounds, str otherwise."""
    if 0 <= i < len(s):
        return s[i]
    return ''


def _move_reph(s):
    """Move a Bangla reph (র + halant, originally appended after its base
    consonant cluster by Bijoy) to the start of the cluster it belongs to.

    Walks left-to-right, advancing past each rewritten reph so we never
    revisit it.
    """
    out = []
    i = 0
    n = len(s)
    while i < n:
        if (
            s[i] == 'র'
            and _at(s, i + 1) == '্'
            and _at(s, i - 1) != '্'
        ):
            j = 1
            while True:
                left = i - j
                if left < 0:
                    break
                if IsBanglaBanjonborno(_at(s, left)) and _at(s, left - 1) == '্':
                    j += 2
                elif j == 1 and IsBanglaKar(_at(s, left)):
                    j += 1
                else:
                    break

            if j >= 1 and (i - j) >= 0 and IsBanglaBanjonborno(_at(s, i - j)):
                pop_count = j
                cluster = ''.join(out[-pop_count:]) if pop_count else ''
                del out[len(out) - pop_count:]
                out.append('র')
                out.append('্')
                out.append(cluster)
                i += 2
                continue
        out.append(s[i])
        i += 1
    return ''.join(out)


def _swap_halant_after_kar(s):
    """Vowel-kar/Nukta + Halant + Consonant → Halant + Consonant + Vowel-kar."""
    out = list(s)
    i = 1
    while i < len(out) - 1:
        if (
            out[i] == '্'
            and (IsBanglaKar(out[i - 1]) or IsBanglaNukta(out[i - 1]))
        ):
            out[i - 1], out[i], out[i + 1] = out[i], out[i + 1], out[i - 1]
            i += 2
            continue
        i += 1
    return ''.join(out)


def _swap_ra_halant_kar(s):
    """RA + Halant + Kar (with no halant before RA) → Kar + RA + Halant."""
    out = list(s)
    i = 1
    while i < len(out) - 1:
        if (
            out[i] == '্'
            and out[i - 1] == 'র'
            and (i - 2 < 0 or out[i - 2] != '্')
            and IsBanglaKar(out[i + 1])
        ):
            out[i - 1], out[i], out[i + 1] = out[i + 1], out[i - 1], out[i]
            i += 2
            continue
        i += 1
    return ''.join(out)


def _move_pre_kars(s):
    """Walk pre-kars (ি ৈ ে) past the following consonant cluster so they
    sit in correct Unicode post-consonant order. Combine ে + া → ো and
    ে + ৗ → ৌ where they meet across the cluster boundary.

    Each pre-kar is processed exactly once: after relocation, ``i`` advances
    past both the original position and the cluster, so the relocated kar is
    never revisited (which previously caused infinite drift to end-of-word).
    """
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if IsBanglaPreKar(c) and i + 1 < n and not IsSpace(s[i + 1]):
            j = 1
            while (i + j) < n - 1 and IsBanglaBanjonborno(_at(s, i + j)):
                if _at(s, i + j + 1) == '্':
                    j += 2
                else:
                    break
            tail_idx = i + j + 1
            l = 0
            if c == 'ে' and _at(s, tail_idx) == 'া':
                pre_repr = 'ো'
                l = 1
            elif c == 'ে' and _at(s, tail_idx) == 'ৗ':
                pre_repr = 'ৌ'
                l = 1
            else:
                pre_repr = c
            cluster = s[i + 1:i + j + 1]
            out.append(cluster)
            out.append(pre_repr)
            i += j + l + 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def _move_nukta_after_kar(s):
    """Nukta belongs after post-kars in Unicode order (nukta + post-kar
    → post-kar + nukta)."""
    out = list(s)
    i = 0
    while i < len(out) - 1:
        if IsBanglaNukta(out[i]) and IsBanglaPostKar(out[i + 1]):
            out[i], out[i + 1] = out[i + 1], out[i]
            i += 2
            continue
        i += 1
    return ''.join(out)


def reArrangeUnicodeConvertedText(str_):
    """Apply Bijoy→Unicode reordering passes in order. Each pass is a single
    left-to-right walk with explicit index advancement, so a transform never
    revisits a slot it just rewrote.
    """
    global proConversionMap

    str_ = _move_reph(str_)
    str_ = doCharMap(str_, proConversionMap)
    str_ = _swap_halant_after_kar(str_)
    str_ = _swap_ra_halant_kar(str_)
    str_ = _move_pre_kars(str_)
    str_ = _move_nukta_after_kar(str_)
    return str_


def doCharMap(text, charMap):
    for k, v in charMap.items():
        pattern = "@{}@".format(k)
        # print(k)
        # print(v)
        # print(charMap)
        text = re.sub(k, v, text)
    return text


# returns the i-th byte of the multi-byte string str
def mbCharAt(s, i):
    return mb_substr(s, i, 1)


# returns the javascript 'substring' method equivalent
def subString(string, from_, to):
    return mb_substr(string, from_, to - from_)


def refactor_broken_kars(s):
    """Swap any pre-kar that ended up *before* its consonant into normal Unicode
    order. Only acts on the broken pattern (pre-kar followed by a consonant);
    pre-kars already in correct post-consonant position are left alone.

    Acts as a final safety net for cases ``reArrangeUnicodeConvertedText`` may
    miss (e.g. pre-kar adjacent to a non-cluster boundary).
    """
    PRE_KARS = ('ি', 'ৈ', 'ে')
    a = list(s)
    last = len(a) - 1
    i = 0
    while i < last:
        if a[i] in PRE_KARS and IsBanglaBanjonborno(a[i + 1]):
            a[i], a[i + 1] = a[i + 1], a[i]
            i += 2
        else:
            i += 1
    return ''.join(a)


# Patterns we never want to remap as Bijoy: URLs, emails, plain Latin words
# embedded in Bangla text (English brand names, file extensions, etc.).
_PROTECTED_RE = re.compile(
    r'https?://\S+'
    r'|ftp://\S+'
    r'|www\.[^\s,;()<>"\'ঀ-৿]+'
    r'|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
)


_SENTINEL_BASE = 0xE000  # Private Use Area — never a Bijoy input or output glyph


def _protect_ascii_runs(text):
    """Replace URLs/emails with single-codepoint PUA sentinels so the Bijoy
    mapper does not chew through their Latin letters. Returns
    ``(masked_text, restorer)``. Caller must invoke ``restorer`` once on the
    final converted string.
    """
    spans = []

    def stash(m):
        idx = len(spans)
        spans.append(m.group(0))
        return chr(_SENTINEL_BASE + idx)

    masked = _PROTECTED_RE.sub(stash, text)

    def restore(s):
        out = s
        for idx, original in enumerate(spans):
            out = out.replace(chr(_SENTINEL_BASE + idx), original)
        return out

    return masked, restore


# main conversion function
def convertBijoyToUnicode(srcString):
    global preConversionMap, conversionMap, postConversionMap
    srcString, restore = _protect_ascii_runs(srcString)
    srcString = doCharMap(srcString, preConversionMap)
    srcString = doCharMap(srcString, conversionMap)
    srcString = reArrangeUnicodeConvertedText(srcString)
    srcString = doCharMap(srcString, postConversionMap)
    srcString = restore(srcString)
    return srcString


