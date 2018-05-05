import re


def mb_substr(s, start, length=None, encoding="UTF-8"):
    u_s = s
    return (u_s[start:(start + length)] if length else u_s[start:]).encode(encoding)


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
    'Í': 'ত্ম',
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
    'æ': 'ম্ন',
    'ç': 'ম্ফ',
    'è': '্ন',
    'é': 'ল্ক',
    'ê': 'ল্গ',
    'ë': 'ল্ট',
    'ì': 'ল্ড',
    'í': 'ল্প',
    'î': 'ল্ফ',
    'ï': 'শু',
    'ð': 'শ্চ',
    'ñ': 'শ্ছ',
    'ò': 'ষ্ণ',
    'ó': 'ষ্ট',
    'ô': 'ষ্ঠ',
    'õ': 'ষ্ফ',
    'ö': 'স্খ',
    '÷': 'স্ট',
    'ø': 'স্ন',  # (sn)eho#†ønØ
    'ù': 'স্ফ',
    'ú': '্প',
    'û': 'হু',
    'ü': 'হৃ',
    'ý': 'হ্ন',
    'þ': 'হ্ম'
}

proConversionMap = {'্্': '্'}

postConversionMap = {
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


def reArrangeUnicodeConvertedText(str_):
    # mb_internal_encoding("UTF-8") # force multi-byte UTF-8 encoding
    global proConversionMap

    for i in range(len(str_)):
        #  Change refs
        if i < (len(str_) - 1) and mbCharAt(str_, i) == 'র' and IsBanglaHalant(
                mbCharAt(str_, i + 1)) and not IsBanglaHalant(mbCharAt(str_, i - 1)):
            j = 1
            while True:
                if i - j < 0:
                    break

                if IsBanglaBanjonborno(mbCharAt(str_, i - j)) and IsBanglaHalant(mbCharAt(str_, i - j - 1)):
                    j += 2
                elif j == 1 and IsBanglaKar(mbCharAt(str_, i - j)):
                    j += 1
                else:
                    break

            temp = subString(str_, 0, i - j)
            temp = temp + mbCharAt(str_, i)
            temp = temp + mbCharAt(str_, i + 1)
            temp = temp + subString(str_, i - j, i)
            temp = temp + subString(str_, i + 2, len(str_))
            str_ = temp
            i += 1
            continue

    str_ = doCharMap(str_, proConversionMap)
    for i in range(len(str_)):
        if i < len(str_) - 1 and mbCharAt(str_, i) == 'র' and IsBanglaHalant(
                mbCharAt(str_, i + 1)) and not IsBanglaHalant(mbCharAt(str_, i - 1)) and IsBanglaHalant(
                mbCharAt(str_, i + 2)):
            j = 1
            while True:
                if i - j < 0:
                    break

                if IsBanglaBanjonborno(mbCharAt(str_, i - j)) and IsBanglaHalant(mbCharAt(str_, i - j - 1)):
                    j += 2
                elif j == 1 and IsBanglaKar(mbCharAt(str_, i - j)):
                    j += 1
                else:
                    break

            temp = subString(str_, 0, i - j)
            temp = temp + mbCharAt(str_, i)
            temp = temp + mbCharAt(str_, i + 1)
            temp = temp + subString(str_, i - j, i)
            temp = temp + subString(str_, i + 2, len(str_))
            str_ = temp
            i += 1
            continue

        # for 'Vowel + HALANT + Consonant' it should be 'HALANT + Consonant + Vowel'
        if i > 0 and mbCharAt(str_, i) == '\u09CD' and (
                    IsBanglaKar(mbCharAt(str_, i - 1)) or IsBanglaNukta(mbCharAt(str_, i - 1))) and i < len(str_) - 1:
            temp = subString(str_, 0, i - 1)
            temp = temp + mbCharAt(str_, i)
            temp = temp + mbCharAt(str_, i + 1)
            temp = temp + mbCharAt(str_, i - 1)
            temp = temp + subString(str_, i + 2, len(str_))
            str_ = temp

        # for 'RA (\u09B0) + HALANT + Vowel' it should be 'Vowel + RA (\u09B0) + HALANT'
        if i > 0 and i < len(str_) - 1 and mbCharAt(str_, i) == '\u09CD' and mbCharAt(str_,
                                                                                      i - 1) == '\u09B0' and mbCharAt(
            str_, i - 2) != '\u09CD' and IsBanglaKar(mbCharAt(str_, i + 1)):
            temp = subString(str_, 0, i - 1)
            temp = temp + mbCharAt(str_, i + 1)
            temp = temp + mbCharAt(str_, i - 1)
            temp = temp + mbCharAt(str_, i)
            temp = temp + subString(str_, i + 2, len(str_))
            str_ = temp

        # Change pre-kar to post format suitable for unicode
        if i < len(str_) - 1 and IsBanglaPreKar(mbCharAt(str_, i)) and IsSpace(mbCharAt(str_, i + 1)) == False:
            temp = subString(str_, 0, i)
            j = 1
            while (i + j) < len(str_) - 1 and IsBanglaBanjonborno(mbCharAt(str_, i + j)):
                if (i + j) < len(str_) and IsBanglaHalant(mbCharAt(str_, i + j + 1)):
                    j += 2
                else:
                    break

            temp = temp + subString(str_, i + 1, i + j + 1)
            l = 0
            if mbCharAt(str_, i) == 'ে' and mbCharAt(str_, i + j + 1) == 'া':
                temp = temp + "ো"
                l = 1
            elif mbCharAt(str_, i) == 'ে' and mbCharAt(str_, i + j + 1) == "ৗ":
                temp = temp + "ৌ"
                l = 1
            else:
                temp = temp + mbCharAt(str_, i)

            temp = temp + subString(str_, i + j + l + 1, len(str_))
            str_ = temp
            i += j

        # nukta should be placed after kars
        if i < len(str_) - 1 and IsBanglaNukta(mbCharAt(str_, i)) and IsBanglaPostKar(mbCharAt(str_, i + 1)):
            temp = subString(str_, 0, i)
            temp = temp + mbCharAt(str_, i + 1)
            temp = temp + mbCharAt(str_, i)
            temp = temp + subString(str_, i + 2, len(str_))
            str_ = temp

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
    a = []
    for i in range(len(s)):
        a.append(s[i])

    b = a[:]
    for i in range(len(a)):
        if a[i] == 'ি':
            b[i] = b[i+1]
            b[i+1] = 'ি'
        elif a[i] == 'ৈ':
            b[i] = b[i+1]
            b[i+1] = 'ৈ'
        elif a[i] == 'ে':
            b[i] = b[i + 1]
            b[i + 1] = 'ে'

    return ''.join(b)


# main conversion function
def convertBijoyToUnicode(srcString):
    global preConversionMap, conversionMap, postConversionMap
    srcString = doCharMap(srcString, preConversionMap)
    srcString = doCharMap(srcString, conversionMap)
    srcString = reArrangeUnicodeConvertedText(srcString)
    srcString = doCharMap(srcString, postConversionMap)

    srcString = refactor_broken_kars(srcString)
    return srcString


