from .spacy_lemmatizer import SpacyLemmatizer
from .persian_lemmatizer import PersianLemmatizer
from .serbian_lemmatizer import ClasslaLemmatizer
from .chinese_lemmatizer import ChineseLemmatizer
from .kazakh_lemmatizer import KazakhLemmatizer

def get_lemmatizer(language):
    language = language.lower()
    if language == 'persian':
        return persian_lemmatizer(language)
    if language == 'serbian':
        return serbian_lemmatizer(language)
    if language == 'chinese':
        return chinese_lemmatizer(language)
    if language in {'english', 'japanese', 'russian', 'spanish', 'french', 'german', 'portuguese'}:
        return spacy_lemmatizer(language)
    if language == 'kazakh':
        from .kazakh_lemmatizer import KazakhLemmatizer
        return kazakh_lemmatizer(language)
    else:
        raise ValueError(f"No lemmatizer available for {language}")
