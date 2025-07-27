from .SpacyLemmatizer import SpacyLemmatizer
from .PersianLemmatizer import PersianLemmatizer
from .ClasslaLemmatizer import ClasslaLemmatizer
from .ChineseLemmatizer import ChineseLemmatizer
from .KazakhLemmatizer import KazakhLemmatizer

def get_lemmatizer(language):
    language = language.lower()
    if language == 'persian':
        return PersianLemmatizer(language)
    if language == 'serbian':
        return ClasslaLemmatizer(language)
    if language == 'chinese':
        return ChineseLemmatizer(language)
    if language in {'english', 'japanese', 'russian', 'spanish', 'french', 'german', 'portuguese'}:
        return SpacyLemmatizer(language)
    if language == 'kazakh':
        from .KazakhLemmatizer import KazakhLemmatizer
        return KazakhLemmatizer(language)
    else:
        raise ValueError(f"No lemmatizer available for {language}")
