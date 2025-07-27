from deep_translator import GoogleTranslator
import fugashi
from pypinyin import pinyin, Style


tagger = fugashi.Tagger()

LANGUAGE_CODES = {
    'japanese': 'ja',
    'chinese': 'zh-cn',
    'russian': 'ru',
    'spanish': 'es',
    'german': 'de',
    'english': 'en'
}

def get_translation(sentence, language):
    translations = {
        'japanese': 'ja',
        'chinese': 'zh-CN',
        'russian': 'ru',
        'spanish': 'es',
        'german': 'de',
        'english': 'en'
    }

    src_lang = translations.get(language.lower())
    if not src_lang:
        return "Unsupported language."

    translator = GoogleTranslator(source=src_lang, target='en')
    return translator.translate(sentence)

def katakana_to_hiragana(katakana):
    return ''.join(
        chr(ord(char) - 0x60) if 'ァ' <= char <= 'ン' else char
        for char in katakana
    )

def get_furigana(sentence):
    words = tagger(sentence)
    furigana_sentence = ''
    for word in words:
        reading = word.feature.kana if word.feature.kana else word.surface
        hiragana_reading = katakana_to_hiragana(reading)
        if word.surface != hiragana_reading:
            furigana_sentence += f"{word.surface}({hiragana_reading})"
        else:
            furigana_sentence += word.surface
    return furigana_sentence


def get_pinyin(text):
    pinyin_tokens = pinyin(text, style=Style.TONE, errors='keep')
    return ' '.join(token[0] for token in pinyin_tokens)


def get_helper_text(sentence, language, helper_type):
    if helper_type == 'translation':
        return get_translation(sentence, language)
    elif helper_type == 'pronunciation' and language == 'japanese':
        return get_furigana(sentence)
    elif helper_type == 'pronunciation' and language == 'chinese':
        return get_pinyin(sentence)
    else:
        return "Helper type not supported for this language."

#test
if __name__ == "__main__":
    test_sentence = "私は日本語を勉強しています。"
    print(get_helper_text(test_sentence, 'japanese', 'translation'))
    print(get_helper_text(test_sentence, 'japanese', 'pronunciation'))
    print(get_helper_text("我喜欢学习新的语言。", 'chinese', 'translation'))
    print(get_helper_text("我喜欢学习新的语言。", 'chinese', 'pronunciation'))